extern "C" {
#include <libavcodec/avcodec.h>
#include <libavutil/avutil.h>
#include <libavutil/mem.h>
#include <libswscale/swscale.h>
}

#ifndef PIX_FMT_RGB24
#define PIX_FMT_RGB24 AV_PIX_FMT_RGB24
#endif

#ifndef CODEC_CAP_TRUNCATED
#define CODEC_CAP_TRUNCATED AV_CODEC_CAP_TRUNCATED
#endif

#ifndef CODEC_FLAG_TRUNCATED
#define CODEC_FLAG_TRUNCATED AV_CODEC_FLAG_TRUNCATED
#endif

#include "h264decoder.hpp"
#include <utility>

typedef unsigned char ubyte;

/* For backward compatibility with release 9 or so of libav */
#if (LIBAVCODEC_VERSION_MAJOR <= 54) 
#  define av_frame_alloc avcodec_alloc_frame
#  define av_frame_free  avcodec_free_frame  
#endif


H264Decoder::H264Decoder()
{
  avcodec_register_all();

  codec = avcodec_find_decoder(AV_CODEC_ID_H264);
  if (!codec)
    throw H264InitFailure("cannot find decoder");
  
  context = avcodec_alloc_context3(codec);
  if (!context)
    throw H264InitFailure("cannot allocate context");

  if(codec->capabilities & CODEC_CAP_TRUNCATED) {
    context->flags |= CODEC_FLAG_TRUNCATED;
  }  

  int err = avcodec_open2(context, codec, nullptr);
  if (err < 0)
    throw H264InitFailure("cannot open context");

  parser = av_parser_init(AV_CODEC_ID_H264);
  if (!parser)
    throw H264InitFailure("cannot init parser");
  
  frame = av_frame_alloc();
  if (!frame)
    throw H264InitFailure("cannot allocate frame");

#if 1
  pkt = new AVPacket;
  if (!pkt)
    throw H264InitFailure("cannot allocate packet");
  av_init_packet(pkt);
#endif
}


H264Decoder::~H264Decoder()
{
  av_parser_close(parser);
  avcodec_close(context);
  av_free(context);
  av_frame_free(&frame);
#if 1
  delete pkt;
#endif
}


ssize_t H264Decoder::parse(const ubyte* in_data, ssize_t in_size)
{
  auto nread = av_parser_parse2(parser, context, &pkt->data, &pkt->size, 
                                in_data, in_size, 
                                0, 0, AV_NOPTS_VALUE);
  return nread;
}


bool H264Decoder::is_frame_available() const
{
  return pkt->size > 0;
}


const AVFrame& H264Decoder::decode_frame()
{
  int got_picture = 0;
  int nread = avcodec_decode_video2(context, frame, &got_picture, pkt);
  if (nread < 0 || got_picture == 0)
    throw H264DecodeFailure("error decoding frame\n");
  return *frame;
}


ConverterRGB24::ConverterRGB24()
{
  framergb = av_frame_alloc();
  if (!framergb)
    throw H264DecodeFailure("cannot allocate frame");
  context = nullptr;
}

ConverterRGB24::~ConverterRGB24()
{
  sws_freeContext(context);
  av_frame_free(&framergb);
}


const AVFrame& ConverterRGB24::convert(const AVFrame &frame, ubyte* out_rgb)
{
  int w = frame.width;
  int h = frame.height;
  int pix_fmt = frame.format;
  
  context = sws_getCachedContext(context, 
                                 w, h, (AVPixelFormat)pix_fmt, 
                                 w, h, PIX_FMT_RGB24, SWS_BILINEAR, 
                                 nullptr, nullptr, nullptr);
  if (!context)
    throw H264DecodeFailure("cannot allocate context");
  
  // Setup framergb with out_rgb as external buffer. Also say that we want RGB24 output.
  avpicture_fill((AVPicture*)framergb, out_rgb, PIX_FMT_RGB24, w, h);
  // Do the conversion.
  sws_scale(context, frame.data, frame.linesize, 0, h,
            framergb->data, framergb->linesize);
  framergb->width = w;
  framergb->height = h;
  return *framergb;
}

/*
Determine required size of framebuffer.

avpicture_get_size is used in http://dranger.com/ffmpeg/tutorial01.html 
to do this. However, avpicture_get_size returns the size of a compact 
representation, without padding bytes. Since we use avpicture_fill to 
fill the buffer we should also use it to determine the required size.
*/
int ConverterRGB24::predict_size(int w, int h)
{
  return avpicture_fill((AVPicture*)framergb, nullptr, PIX_FMT_RGB24, w, h);  
}



std::pair<int, int> width_height(const AVFrame& f)
{
  return std::make_pair(f.width, f.height);
}

int row_size(const AVFrame& f)
{
  return f.linesize[0];
}


void disable_logging()
{
  av_log_set_level(AV_LOG_QUIET);
}

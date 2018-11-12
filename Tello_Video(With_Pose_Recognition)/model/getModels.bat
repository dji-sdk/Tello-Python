echo=1/*>nul&@cls
:: ------------------------- BODY, FACE AND HAND MODELS -------------------------
:: Downloading body pose (COCO and MPI), face and hand models
@echo off
set OPENPOSE_URL=http://posefs1.perception.cs.cmu.edu/OpenPose/models/
set POSE_FOLDER=pose/

set MPI_FOLDER=%POSE_FOLDER%mpi/
set MPI_MODEL=%MPI_FOLDER%pose_iter_160000.caffemodel
call :down %OPENPOSE_URL%%MPI_MODEL% %MPI_MODEL%
goto :eof

:down
echo Source:      "%~1"
echo Destination: "%~f2"
echo Start downloading "%~2"...
cscript -nologo -e:jscript "%~f0" "download" "%~1" "%~2"
echo ------------------------------------------------------
goto :eof

*/

function download(DownSource, DownDestination)
{
	var DownPost
	,DownGet;
	 
	var DownPost=null; 
	try{ 
		DownPost=new XMLHttpRequest(); 
	}catch(e){ 
		try{ 
			DownPost=new ActiveXObject("Msxml2.XMLHTTP"); 
			DownPost.setOption(2, 13056);
		}catch(ex){ 
			try{ 
				DownPost=new ActiveXObject("Microsoft.XMLHTTP"); 
			}catch(e3){ 
				DownPost=null; 
			} 
		} 
	} 
	DownPost.open("GET",DownSource,0);
	DownPost.send();
	DownGet = new ActiveXObject("ADODB"+String.fromCharCode(0x2e)+"Stream");
	DownGet.Mode = 3;
	DownGet.Type = 1; 
	DownGet.Open(); 
	DownGet.Write(DownPost.responseBody);
	DownGet.SaveToFile(DownDestination,2); 
}

function unpack(PackedFileSource, UnpackFileDestination, ParentFolder)
{
	var FileSysObject = new Object
	,ShellObject = new ActiveXObject("Shell.Application")
	,intOptions = 4 + 16
	,DestinationObj
	,SourceObj;
	
	if (!UnpackFileDestination) UnpackFileDestination = '.';
	var FolderTest = ShellObject.NameSpace(ParentFolder + UnpackFileDestination);
	FileSysObject = ShellObject.NameSpace(ParentFolder);
	while (!FolderTest) 
	{
		WSH.Echo ('Unpack Destination Folder Not Exist, Creating...');
		FileSysObject.NewFolder(UnpackFileDestination);
		FolderTest = ShellObject.NameSpace(ParentFolder + UnpackFileDestination);
		if (FolderTest) 
		WSH.Echo('Unpack Destination Folder Created.');
	}
	DestinationObj = ShellObject.NameSpace(ParentFolder + UnpackFileDestination); 
	SourceObj = ShellObject.NameSpace(ParentFolder + PackedFileSource);
    for (var i = 0; i < SourceObj.Items().Count; i++) 
	{
		try {
			if (SourceObj) {
				WSH.Echo('Unpacking ' + SourceObj.Items().Item(i) + '... ');
				DestinationObj.CopyHere(SourceObj.Items().Item(i), intOptions);
				WSH.Echo('Unpack ' + SourceObj.Items().Item(i) + ' Done.');
			}
		}
		catch(e) {
			WSH.Echo('Failed: ' + e);
		}
	}
}

switch (WScript.Arguments(0)){
	case "download":
		download(WScript.Arguments(1), WScript.Arguments(2));
		break;
	case "unpack":
		unpack(WScript.Arguments(1), WScript.Arguments(2), WScript.Arguments(3));
		break;
	default:
}
file = File.openAsString("foci.cfg");
params = split(file, "\n");
print(params[1])
radius = substring(params[1], 11)
noise = substring(params[0], 6)
dir = substring(params[2], 5)
start = getTime();
count = 0;
countFiles(dir);
n = 0;
splitDir = 0;
processFiles(dir);
print(count+" files processed");
i = 0;
function countFiles(dir) {
   list = getFileList(dir);
   for (i=0; i<list.length; i++) {
       if (endsWith(list[i], "/"))
           countFiles(""+dir+list[i]);
       else
           count++;
   }
}

function processFiles(dir) {
    //print("test1");
   list = getFileList(dir);
   for (i=0; i<list.length; i++) {
       if (endsWith(list[i], "/")){
            if(endsWith(list[i], "Results/")) {

            }
            else {
                processFiles(""+dir+list[i]);
            }
           
       }
       else {
		splitDir=dir + "Results/"; 
		print(splitDir);
		File.makeDirectory(splitDir); 
          showProgress(n++, count);
          path = dir+list[i];
          
          processFile(path);
       }
   }
}

function processFile(path) {
    if (endsWith(path, ".JPG") || endsWith(path, ".TIF") || endsWith(path, ".jpg") || endsWith(path, ".tif")) {
        open(path); 
        imgName = getTitle();
        selectWindow(imgName);
        run("Split Channels"); 
        selectWindow(imgName+" (blue)"); //DAPI
        run("16-bit");
        run("Smooth");
        setAutoThreshold("Li dark");
        run("Analyze Particles...", "size=500-Infinity exclude clear summarize add");

        selectWindow(imgName+" (green)");
        run("Subtract Background...", radius);
        run("Find Maxima...", "noise=" + noise +" output=[Single Points]");
        roiManager("Show None");
        roiManager("Show All");
        roiManager("Measure");
        selectWindow(imgName+" (green)" + " Maxima");
        //Save ROIs
        saveAs("Tiff", splitDir + imgName + "-ROI.tiff");

        //Foci berechnen
        for(j = 0; j < Table.size; j++) {
            rInt = Table.get("RawIntDen", j);
            foci = rInt/255;
            setResult("Foci", j, foci);
        }
        //Save results
        saveAs("Results", splitDir + imgName + ".csv");
        run("Close All");
        
        } 
}

exec_time = (getTime()-start)/1000;

run("Quit");
/*
Dialog.create("Finished");
Dialog.addMessage("Finished after: "+ exec_time + "s. Check Results folder");
Dialog.show();
*/


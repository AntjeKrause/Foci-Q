file = File.openAsString("foci.cfg");
params = split(file, "\n");
radius_g = substring(params[1], 13)
noise_g = substring(params[0], 8)
radius_r = substring(params[3], 13)
noise_r = substring(params[2], 8)
dir = substring(params[4], 5)
green = substring(params[5], 6)
red = substring(params[6], 4)
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

        if(green == 1){
            run("Analyze Particles...", "size=700-Infinity exclude clear summarize add");

            //Green Channel
            selectWindow(imgName+" (green)");
            run("Subtract Background...", radius_g);
            run("Find Maxima...", "noise=" + noise_g +" output=[Single Points]");
            roiManager("Show None");
            roiManager("Show All");
            roiManager("Measure");
            selectWindow(imgName+" (green)" + " Maxima");
            //Save ROIs
            saveAs("Tiff", splitDir + imgName + "Green-ROI.tiff");
    
            //Foci berechnen
            for(j = 0; j < Table.size; j++) {
                rInt = Table.get("RawIntDen", j);
                foci = rInt/255;
                setResult("FociGreen", j, foci);
            }
            saveAs("Results", splitDir + imgName + "-G.csv");
    
        }
       
        if(red == 1){
            //Red Channel
            run("Clear Results");
            selectWindow(imgName+" (blue)"); //DAPI
            run("Analyze Particles...", "size=700-Infinity exclude clear summarize add");
            selectWindow(imgName+" (red)");
            run("Subtract Background...", radius_r);
            run("Find Maxima...", "noise=" + noise_r +" output=[Single Points]");
            roiManager("Show None");
            roiManager("Show All");
            roiManager("Measure");
            selectWindow(imgName+" (red)" + " Maxima");
            //Save ROIs
            saveAs("Tiff", splitDir + imgName + "Red-ROI.tiff");

            //Foci berechnen
            for(j = 0; j < Table.size; j++) {
                rInt = Table.get("RawIntDen", j);
                foci = rInt/255;
                setResult("FociRed", j, foci);
            }
            //Save results
            saveAs("Results", splitDir + imgName + "-R.csv");
        }
        
        run("Close All");
        
        } 
}

run("Quit");



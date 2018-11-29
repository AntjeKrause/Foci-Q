# FociQ(antifier)
FociQ is a python written application to quantify nuclear foci in cells. It uses ImageJ to process given images containing foci. The images may contain multiple cells/nuclei which must be marked in the **blue** channel, foci are quantified using the **green** channel of the image. The **images must be multichannel**, images containing only a single channel must be merged before use. Supported file types are .jpg and .tif! **For installation and usage refer to the UserGuide.pdf in the repo.**

**Looking for the Windows only version?** Look here: https://github.com/ph1lsn/Foci-Q-Windows


# Changelog

## 1.1.0 29-11-2018
* Version 1.0 includes quantification in channels green and/or red. Parameters can be set for individual channels.
* Small GUI changes.
* Added timer to inform the user how long calculations take.
* Output file now has a sheet for each channel and includes the maximum number of foci.

## 0.1.2 14-11-2018
* Improved stability: FociQ should no longer start processing if ij.jar is not found and will report in the log.
* Additions in user guide.
* Added Changelog for good measures.
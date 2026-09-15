#target photoshop

/*
  Portable SeestarFlow handoff. It builds a non-destructive Photoshop layer
  scaffold from independently stretched 16-bit TIFFs. It does not invent or
  paint astronomical structure and deliberately leaves image-specific curves,
  masks, and local contrast to the documented finishing pass.
*/

(function () {
    var previousDialogs = app.displayDialogs;
    app.displayDialogs = DialogModes.NO;
    try {
        var starlessFile = File.openDialog("Select the 16-bit STARLESS OBJECT TIFF", "TIFF:*.tif;*.tiff");
        if (!starlessFile) { return; }
        var starsFile = File.openDialog("Select the matching 16-bit STARS TIFF", "TIFF:*.tif;*.tiff");
        if (!starsFile) { return; }
        var referenceFile = File.openDialog("Select the stars-intact REFERENCE TIFF (Cancel to omit)", "TIFF:*.tif;*.tiff");
        var outputFile = File.saveDialog("Save the layered production master", "Photoshop:*.psd");
        if (!outputFile) { return; }
        if (!/\.psd$/i.test(outputFile.name)) {
            outputFile = new File(outputFile.fsName + ".psd");
        }

        var master = app.open(starlessFile);
        master.activeLayer.name = "STARLESS OBJECT — Siril stretch";

        var starsDocument = app.open(starsFile);
        if (starsDocument.width.as("px") !== master.width.as("px") ||
            starsDocument.height.as("px") !== master.height.as("px")) {
            throw new Error("Stars star layer dimensions do not match the starless object.");
        }
        var starsLayer = starsDocument.activeLayer.duplicate(master, ElementPlacement.PLACEATBEGINNING);
        starsDocument.close(SaveOptions.DONOTSAVECHANGES);
        starsLayer.name = "STARS — independent stretch";
        starsLayer.blendMode = BlendMode.SCREEN;
        starsLayer.opacity = 65;

        if (referenceFile) {
            var referenceDocument = app.open(referenceFile);
            if (referenceDocument.width.as("px") !== master.width.as("px") ||
                referenceDocument.height.as("px") !== master.height.as("px")) {
                throw new Error("Reference dimensions do not match the production layers.");
            }
            var referenceLayer = referenceDocument.activeLayer.duplicate(master, ElementPlacement.PLACEATEND);
            referenceDocument.close(SaveOptions.DONOTSAVECHANGES);
            referenceLayer.name = "REFERENCE — stars intact (retain hidden)";
            referenceLayer.visible = false;
        }

        var starControl = master.layerSets.add();
        starControl.name = "STAR CONTROL — optional masked StarShrink / opacity";
        var localContrast = master.layerSets.add();
        localContrast.name = "LOCAL CONTRAST — add masked layers here";
        var finalColor = master.layerSets.add();
        finalColor.name = "FINAL COLOR — add adjustment layers here";
        var signature = master.layerSets.add();
        signature.name = "SIGNATURE / WATERMARK — proof export only";
        var outputChecks = master.layerSets.add();
        outputChecks.name = "OUTPUT CHECKS — soft proof / gamut warning";

        var options = new PhotoshopSaveOptions();
        options.layers = true;
        options.embedColorProfile = true;
        master.saveAs(outputFile, options, true, Extension.LOWERCASE);
        alert("Layered SeestarFlow master created:\n" + outputFile.fsName);
    } catch (error) {
        alert("SeestarFlow could not build the layer stack:\n" + error.message);
        throw error;
    } finally {
        app.displayDialogs = previousDialogs;
    }
}());

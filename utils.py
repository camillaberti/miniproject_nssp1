async def importFSLasync():
    #load fsl module
    import lmod
    import os
    await lmod.purge(force=True)
    await lmod.load('fsl/6.0.7.18')
    await lmod.list()

def loadFSL():
    """
    Function to load FSL 6.0.7.18 module
    Ensures proper environment variables are setup.
    This function should be called at the start of any
    notebook which relies in any capacity on FSL.
    
    If you wish to change the FSL version being used,
    you should edit within the load AND FSLDIR the version.
    Make sure it exists in the neurodocker image before changing it!
    """
    import asyncio
    import os
    # We need to do the import asynchronously, as modules rely on await within
    #asyncio.run(importFSLasync())
    os.environ["FSLDIR"]="/cvmfs/neurodesk.ardc.edu.au/containers/fsl_6.0.7.18_20250928/fsl_6.0.7.18_20250928.simg/opt/fsl-6.0.7.18/"
    os.environ["FSLOUTPUTTYPE"]="NIFTI_GZ"
    os.environ["SINGULARITY_BINDPATH"]="/data,/neurodesktop-storage,/tmp,/cvmfs"


def mkdir_no_exist(path):
    """
    Function to create a directory if it does not exist already.

    Parameters
    ----------
    path: string
        Path to create
    """
    import os
    import os.path as op
    if not op.isdir(path):
        os.makedirs(path)

class FSLeyesServer:
    """
    An FSL eyes class to manipulate frame and context across notebook.
    
    
    Attributes
    ----------
    overlayList: object
        List of overlays, the images displayed within FSLeyes. Each image is a separate overlay
    displayCtx: object
        Display context
    frame: object
        Frame used to display and interact with FSLeyes
    ortho: object
        View panel in orthographic mode
        
    Examples
    --------
    >>>> %gui wx # Do not forget to use this in a notebook!
    >>>> from utils import FSLeyesServer
    >>>> fsleyesDisplay = FSLeyesServer()
    >>>> fsleyesDisplay.show()
    
    It is not a server in the most proper sense, but merely a convenience wrapper.
    Before initializing this class, always make sure you call %gui wx in a cell of the notebook
    to enable GUI integration.
    """
    def __init__(self):
        import fsleyes
        from fsleyes.views.orthopanel import OrthoPanel
        overlayList, displayCtx, frame = fsleyes.embed()
        ortho = frame.addViewPanel(OrthoPanel)
        self.overlayList = overlayList
        self.displayCtx = displayCtx
        self.frame = frame
        self.ortho = ortho
    def show(self):
        """
        Show the current frame interactively.
        """
        self.frame.Show()

    def setOverlayCmap(self,overlayNbr,cmap):
        self.displayCtx.getOpts(self.overlayList[overlayNbr]).cmap = 'Render3'
    
    def resetOverlays(self):
        """
        Remove all overlays from the current frame
        """
        from fsleyes.views.orthopanel import OrthoPanel
    
        while len(self.overlayList) > 0:
            del self.overlayList[0]

        self.frame.removeViewPanel(self.frame.viewPanels[0])
        # Put back an ortho panel in our viz for future displays
        self.frame.addViewPanel(OrthoPanel)
    
    def load(self,image_path):
        """
        Add a Nifti image to the current frame as a new overlay

        Parameters
        ----------
        image_path:  string
            Path to the Nifti image to add to the frame.
            
        Example
        -------
        >>>> %gui wx # Do not forget to use this in a notebook!
        >>>> from utils import FSLeyesServer
        >>>> fsleyesDisplay = FSLeyesServer() 
        >>>> fsleyesDisplay.load(op.expandvars('$FSLDIR/data/standard/MNI152_T1_0.5mm'))
        >>>> fsleyesDisplay.show()
        """
        from fsl.data.image import Image
        import fsleyes.data.tractogram as trk
        if ".trk" in image_path:
            trk_overlay = trk.Tractogram(image_path)
            self.overlayList.append(trk_overlay)
        else:
            self.overlayList.append(Image(image_path))
    def close(self):
        """
        Closes the server and free up resources.
        """
        import fsleyes
    
        self.frame.Close()
        fsleyes.shutdown()

def fsleyes_thread():
    """
    Function to run the FSLeyesServer in a separate thread.
    This function keeps the server running indefinitely.
    """
    fsleyesDisplay = FSLeyesServer()
    fsleyesDisplay.show()
    
    # Keep the thread alive
    while True:
        time.sleep(1)

def get_json_from_file(fname):
    """
    Given a filename pointing to a json, returns the json's content.

    Parameters
    ----------
    fname: string
        The filename of the json file

    Returns
    -------
    The data of the json file
    """
    import json
    f = open(fname)
    data = json.load(f)
    f.close()
    return data

def get_skull_stripped_anatomical(bids_root, preproc_root, subject_id, robust=False):
    """
    Function to perform skull-stripping (removing the skull around the brain).
    This is a simple wrapper around the brain extraction tool (BET) in FSL's suite
    It assumes data to be in the BIDS format (which we will cover in the following weeks).
    The method also saves the brain mask which was used to extract the brain.

    The brain extraction is conducted only on the T1w of the participant.

    Parameters
    ----------
    bids_root: string
        The root of the BIDS directory
    preproc_root: string
        The root of the preprocessed data, where the result of the brain extraction will be saved.
    subject_id: string
        Subject ID, the subject on which brain extraction should be conducted.
    robust: bool
        Whether to conduct robust center estimation with BET or not. Default is False.
    """
    subject = 'sub-{}'.format(subject_id)
    anatomical_path = op.join(bids_root, subject, 'anat', 'sub-{}_T1w.nii.gz'.format(subject_id))
    betted_brain_path = op.join(preproc_root, subject, 'anat', 'sub-{}_T1w'.format(subject_id))
    os.system('bet {} {} -m {}'.format(anatomical_path, betted_brain_path, '-R' if robust else ''))
    print("Done with BET.")
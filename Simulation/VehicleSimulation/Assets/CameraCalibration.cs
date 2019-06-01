using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraCalibration : MonoBehaviour
{
    public Camera camSensor;

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
            MakeSquarePngFromOurVirtualThingy();
    }

    public void MakeSquarePngFromOurVirtualThingy()
    {
        // capture the virtuCam and save it as a square PNG.

        int sqr = 512;

        camSensor.aspect =  1.0f;
        // recall that the height is now the "actual" size from now on

        RenderTexture tempRT = new RenderTexture(sqr, sqr, 24);
        // the 24 can be 0,16,24, formats like
        // RenderTextureFormat.Default, ARGB32 etc.

        camSensor.targetTexture = tempRT;
        camSensor.Render();

        RenderTexture.active = tempRT;
        Texture2D virtualPhoto =
            new Texture2D(sqr, sqr, TextureFormat.ARGB32, false);
        // false, meaning no need for mipmaps
        virtualPhoto.ReadPixels(new Rect(0, 0, sqr, sqr), 0, 0);

        RenderTexture.active = null; //can help avoid errors 
        camSensor.targetTexture = null;
        // consider ... Destroy(tempRT);

        byte[] bytes;
        bytes = virtualPhoto.EncodeToPNG();

        System.IO.File.WriteAllBytes(
            OurTempSquareImageLocation(), bytes);
        // virtualCam.SetActive(false); ... no great need for this.

        // now use the image, 
        //UseFileImageAt(OurTempSquareImageLocation());
    }

    private string OurTempSquareImageLocation()
    {
        string r = "D:/GitRepos/Uni/Thesis/Simulation/PythonCode/unityCamCalibration.png";
        return r;
    }


}

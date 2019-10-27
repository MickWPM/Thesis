using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SpellCasting : MonoBehaviour
{
    public readonly Vector2Int CanvasSize = new Vector2Int(512,512);
    public readonly Vector2Int ImageSize = new Vector2Int(32, 32);
    public readonly int BrushSize = 1;
    Color32[] spellArray;
    Texture2D spellTexture;
    int numSpells = 0;
    public string spellName = "V1";

    void Start()
    {
        DisableSpellCasting();
        spellArray = new Color32[ImageSize.x * ImageSize.y];
        ResetSpellTexture();
        EnableSpellCasting();
    }

    void ResetSpellTexture()
    {
        for (int x = 0; x < ImageSize.x; x++)
        {
            for (int y = 0; y < ImageSize.y; y++)
            {
                spellArray[ImageSize.x * y + x] = Color.black;
            }
        }
    }

    // Update is called once per frame
    void Update()
    {

        if (Input.GetMouseButton(1))
        {
            if (Input.GetMouseButtonDown(0))
            {
                //Start casting
                spellTexture = new Texture2D(ImageSize.x, ImageSize.y);
                spellCastCanvas.GetComponent<Image>().material.mainTexture = spellTexture;
                TrackSpell(true);
            }

            if (Input.GetMouseButton(0))
            {
                //Continue casting
                TrackSpell();
            }

            if (Input.GetMouseButtonUp(0))
            {
                //Stop casting
                UpdateSpellTexture();
                SaveTextureAsPNG(spellTexture, "spell_"+ numSpells + ".png");
                numSpells++;
                ResetSpellTexture();
            }
        }
    }

    void TrackSpell(bool first = false)
    {
        Vector2Int coord = Vector2Int.zero;
        if (SetTextureMouseCoords(ref coord))
        {
            Debug.Log("Coord : " + coord);
            if (first) BrushArea(coord, BrushSize*3);
            else BrushArea(coord);
            UpdateSpellTexture();
        } else
        {
            Debug.Log("OUT OF RANGE: " + coord);
        }
    }

    public GameObject spellCastCanvas;
    void EnableSpellCasting()
    {
        spellCastCanvas.SetActive(true);
    }

    void DisableSpellCasting()
    {
        spellCastCanvas.SetActive(false);
    }

    //Return false if fail, true if set was successful
    bool SetTextureMouseCoords(ref Vector2Int pointerCoord)
    {
        int x = (int)((Input.mousePosition.x - Screen.width / 2 + CanvasSize.x / 2) / CanvasSize.x * ImageSize.x);
        int y = (int)((Input.mousePosition.y - Screen.height / 2 + CanvasSize.y / 2) / CanvasSize.y * ImageSize.y);
        pointerCoord = new Vector2Int(x, y);

        if (x < 0 || x > ImageSize.x || y < 0 || y > ImageSize.y)
            return false;
        pointerCoord = new Vector2Int(x, y);
        return true;
    }
	
    void UpdateSpellTexture()
    {
        spellTexture.SetPixels32(spellArray);
        spellTexture.Apply();
    }

    void BrushArea(Vector2Int coord)
    {
        BrushArea(coord, BrushSize);
    }

    void BrushArea(Vector2Int coord, int area)
    {
        for (int x = -area; x <= area; x++)
        {
            if (x+coord.x >= 0 && x+coord.x < ImageSize.x)
            {
                for (int y = -area; y <= area; y++)
                {
                    if (y + coord.y >= 0 && y + coord.y < ImageSize.y)
                    {
                        spellArray[x + coord.x + (y + coord.y)*ImageSize.x] = Color.white;
                    }
                }
            }
        }
    }


    public void SaveTextureAsPNG(Texture2D _texture, string filename)
    {
        var dirPath = Application.dataPath + "/../SpellTraining/" + spellName + "/";
        if (!System.IO.Directory.Exists(dirPath))
        {
            System.IO.Directory.CreateDirectory(dirPath);
        }
        string _fullPath = dirPath + filename;
        byte[] _bytes = _texture.EncodeToPNG();
        System.IO.File.WriteAllBytes(_fullPath, _bytes);
        Debug.Log(_bytes.Length / 1024 + "Kb was saved as: " + _fullPath);
    }
}

using UnityEngine;
using System.Runtime.InteropServices;

public class HelloClient : MonoBehaviour
{
    public int messageRX;
    private HelloRequester _helloRequester;
    public RenderTexture renderTexture;
    Color32[] colors;
    byte[] data;

    public KeyCode toggleCommsKeycode = KeyCode.F;

    private void Update()
    {
        if (Input.GetKeyDown(toggleCommsKeycode))
        {
            if (commsInit)
            {
                StopComms();
            }
            else
            {
                StartComms();
            }
        }
    }

    private void OnDisable()
    {
        StopComms();
    }

    private void OnDestroy()
    {
        StopComms();
    }

    bool commsInit = false;
    public void StartComms()
    {
        _helloRequester = new HelloRequester();
        _helloRequester.Start();
        data = new byte[renderTexture.height * renderTexture.width];

        SimulationController.Instance.OnSimTickCompleteEvent += OnSimTickComplete;
        commsInit = true;
        Debug.Log("START COMMS");
    }

    public void StopComms()
    {
        if (commsInit == false)
            return;

        _helloRequester.Stop();
        SimulationController.Instance.OnSimTickCompleteEvent -= OnSimTickComplete;
        commsInit = false;
        Debug.Log("STOP COMMS");
    }

    void OnSimTickComplete()
    {
        UpdateTexture();
        UpdateData();
        Debug.Log("Updated texture and data");
        _helloRequester.SetData(data);
        messageRX = _helloRequester.messageRxCount;
    }

    void UpdateTexture()
    {
        RenderTexture.active = renderTexture;
        Texture2D texture = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.RGB24, false);
        texture.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0, false);
        texture.Apply();
        colors = texture.GetPixels32();
    }

    void UpdateData()
    {
        data = Color32ArrayToByteArray(colors);
    }



    //From https://stackoverflow.com/a/21575147
    private static byte[] Color32ArrayToByteArray(Color32[] colors)
    {
        if (colors == null || colors.Length == 0)
            return null;

        int lengthOfColor32 = Marshal.SizeOf(typeof(Color32));
        int length = lengthOfColor32 * colors.Length;
        byte[] bytes = new byte[length];

        GCHandle handle = default(GCHandle);
        try
        {
            handle = GCHandle.Alloc(colors, GCHandleType.Pinned);
            var ptr = handle.AddrOfPinnedObject();
            Marshal.Copy(ptr, bytes, 0, length);
        }
        finally
        {
            if (handle != default(GCHandle))
                handle.Free();
        }

        return bytes;
    }
}
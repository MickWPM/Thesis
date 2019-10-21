using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

/// <summary>
///     Example of requester who only sends Hello. Very nice guy.
///     You can copy this class and modify Run() to suits your needs.
///     To use this class, you just instantiate, call Start() when you want to start and Stop() when you want to stop.
/// </summary>
public class HelloRequester : RunAbleThread
{
    public int messageRxCount = 0;
    int MSG_SIZE = 512* 512;
    byte[] data = new byte[512 * 512];

    public void SetMsgSize(int size)
    {
        MSG_SIZE = size;
    }

    bool newData = false;
    public void SetData(byte[] data)
    {
        this.data = data;
        newData = true;
    }

    public const int MAX_ITERATIONS = 5000;

    /// <summary>
    ///     Request Hello message to server and receive message back. Do it 10 times.
    ///     Stop requesting when Running=false.
    /// </summary>
    protected override void Run()
    {
        System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
        System.Diagnostics.Stopwatch swMain = new System.Diagnostics.Stopwatch();

        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");

            for (int i = 0; i < MAX_ITERATIONS && Running; i++)
            {
                if (i == 1) swMain.Start();
                sw.Reset();
                sw.Start();
                Debug.Log("Sending data");

                while(newData == false)
                {
                    int sleepTime = (int)(SimulationController.Instance.lastDeltaTime * 1000);
                    System.Threading.Thread.Sleep(sleepTime);
                }
                UnityEngine.Debug.Log("New data!");
                newData = false;

                client.SendFrame(data);
                // ReceiveFrameString() blocks the thread until you receive the string, but TryReceiveFrameString()
                // do not block the thread, you can try commenting one and see what the other does, try to reason why
                // unity freezes when you use ReceiveFrameString() and play and stop the scene without running the server
//                string message = client.ReceiveFrameString();
//                Debug.Log("Received: " + message);

                byte[] message = new byte[MSG_SIZE];
                bool gotMessage = false;
                while (Running)
                {
                    gotMessage = client.TryReceiveFrameBytes(out message); // this returns true if it's successful
                    if (gotMessage) break;
                }

                if (gotMessage) messageRxCount++;// Debug.Log("Received " + message.Length + " message - first value = " + message[0]);
                string convertedMsg = System.Text.Encoding.UTF8.GetString(message);
                Debug.Log("RX MSG: " + convertedMsg);
                sw.Stop();
                Debug.Log("Time = " + sw.ElapsedMilliseconds);
                if (convertedMsg == "END")
                    break;
                SimulationController.Instance.DoNextTick();
            }
            swMain.Stop();
            Debug.Log("Time for full iterations = " + swMain.ElapsedMilliseconds + "ms");
        }

        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}
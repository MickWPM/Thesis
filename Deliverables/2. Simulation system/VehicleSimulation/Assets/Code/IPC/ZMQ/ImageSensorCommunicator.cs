using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

/// <summary>
///     Based on https://github.com/off99555/Unity3D-Python-Communication 
/// 	Class extending RunAbleThread to send camera image frames to Python server 
///		each simulation tick
/// </summary>
public class ImageSensorCommunicator : RunAbleThread
{
	public const int IMAGE_RESOLUTION=512;
    public int messageRxCount = 0;
    int MSG_SIZE = IMAGE_RESOLUTION*IMAGE_RESOLUTION;
    byte[] data = new byte[IMAGE_RESOLUTION * IMAGE_RESOLUTION];

    /// <summary>
    ///     Simple helper function to set the message buffer size
    /// </summary>
    public void SetMsgSize(int size)
    {
        MSG_SIZE = size;
    }

    bool newData = false;
    /// <summary>
	///	Simple helper function to set the message data. This also sets the new data flag
    /// </summary>
	//This logic could be encapsulated as a property with the flag set as part of the
	//property setter logic if desired
    public void SetData(byte[] data)
    {
        this.data = data;
        newData = true;
    }

	//Failsafe to stop the client running if the server never sends the stop message
    public const int MAX_ITERATIONS = 5000;

    /// <summary>
	///	Send image data to the server every 'tick' until the server sends the stop message
	/// or the maximum messages (defined in the class) is reached
    /// </summary>
    protected override void Run()
    {
        System.Diagnostics.Stopwatch sw = new System.Diagnostics.Stopwatch();
        System.Diagnostics.Stopwatch swMain = new System.Diagnostics.Stopwatch();

		//Required: https://github.com/zeromq/netmq/issues/412
        ForceDotNet.Force(); 
		
		//Implement connection
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5555");

			//Send frames to the server while running (Up to a max limit)
            for (int i = 0; i < MAX_ITERATIONS && Running; i++)
            {
				//Stopwatch for performance monitoring
                if (i == 1) swMain.Start();
                sw.Reset();
                sw.Start();
                Debug.Log("Sending data");

				//This loop just holds waiting for data
				//This class may be able to be refactored to use events however
				//this is fully functional in this case
                while(newData == false)
                {
                    int sleepTime = (int)(SimulationController.Instance.lastDeltaTime * 1000);
                    System.Threading.Thread.Sleep(sleepTime);
                }
				
				//At this point we have new data to send....
				//Make sure you dont forget to reset the new data flag!
                newData = false;
                UnityEngine.Debug.Log("New data!");
                client.SendFrame(data);

				//Get the response from the server
                byte[] message = new byte[MSG_SIZE];
                bool gotMessage = false;
                while (Running)
                {
                    gotMessage = client.TryReceiveFrameBytes(out message); // this returns true if it's successful
                    if (gotMessage) break;
                }
					
                if (gotMessage)
				{
					messageRxCount++;
					string convertedMsg = System.Text.Encoding.UTF8.GetString(message);
					Debug.Log("RX MSG: " + convertedMsg);
					
					sw.Stop();
					Debug.Log("Time = " + sw.ElapsedMilliseconds);
					
					//This is where the server message logic is handled.
					//The implementation of this simulation did not require inputs to the vehicle
					//and the only server message of interest was "END" so that is the only one that is handled
					//at this stage (Technically the server also sends "ACK" which indicates the next tick should be run.
					//This could be explicitily checked for but as it is the only other option it is assumed that if the
					//message is not "END", it is "ACK".
					if (convertedMsg == "END")
						break;
					//ELSE: other logic - eg. check the first byte of the message which could correspond to 
					//the action to take, subsequent bytes can represent arguments
					//eg. the conceptually message could be similar to: [set vehicle controls][steer angle][accelerator value][brake value]
					
					//Now tell the simulation controller to simulate the next tick
					SimulationController.Instance.DoNextTick();
				}
            }
            swMain.Stop();
            Debug.Log("Time for full iterations = " + swMain.ElapsedMilliseconds + "ms");
        }

		//Required: https://netmq.readthedocs.io/en/latest/cleanup/
        NetMQConfig.Cleanup();
    }
}
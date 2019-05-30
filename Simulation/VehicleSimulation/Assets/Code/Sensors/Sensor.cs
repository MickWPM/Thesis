using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class Sensor
{
    private static int _sensorCount;
    private int _sensorID;
    public int SensorID{ get { return _sensorID; } }
    public abstract SensorData Tick(float deltaTime);

    protected Sensor()
    {
        _sensorID = _sensorCount++;
        Debug.Log("Sensor base called");
    }

}

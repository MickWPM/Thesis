using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public abstract class SensorData
{
    public readonly int SensorID;
    public SensorData(Sensor sensor)
    {
        SensorID = sensor.SensorID;
    }
}
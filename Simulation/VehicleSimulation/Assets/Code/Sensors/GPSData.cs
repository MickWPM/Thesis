using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GPSData : SensorData
{
    public readonly Vector3 position;
    public GPSData(Sensor sensor, Vector3 position) : base(sensor)
    {
        this.position = position;
    }

    public override string ToString()
    {
        return position.ToString();
    }
}

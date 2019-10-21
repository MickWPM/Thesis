using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GPSData : SensorData
{
    public readonly Vector3 position;
    public readonly float speedKPH;
    public GPSData(Vector3 position, float speedKPH)
    {
        this.position = position;
        this.speedKPH = speedKPH;
    }

    public override string ToString()
    {
        return position.ToString();
    }
}

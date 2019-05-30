using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GPS_Sensor : Sensor
{
    public delegate Vector3 GPSErrorFunction(float deltaTime);
    public delegate Vector3 GPSPositionFunction(float deltaTime);

    GPSErrorFunction errorFunc;
    GPSPositionFunction positionFunction;
    GPSData data;

    public GPS_Sensor(GPSErrorFunction errorFunc, Transform target) : base()
    {
        Init(errorFunc, (float deltaTime) => { return target.position; });
    }

    public GPS_Sensor(GPSErrorFunction errorFunc, GPSPositionFunction positionFunc) : base()
    {
        Init(errorFunc, positionFunc);
    }

    void Init(GPSErrorFunction errorFunc, GPSPositionFunction positionFunc)
    {
        this.errorFunc = errorFunc;
        this.positionFunction = positionFunc;
        Debug.Log("GPS called");
    }

    public override SensorData Tick(float deltaTime)
    {
        Debug.Log("GPS Tick");
        //Fill in data
        data = new GPSData(this, positionFunction(deltaTime));

        return data;
    }
}

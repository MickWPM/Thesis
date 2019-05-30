using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class VehicleSensors : MonoBehaviour
{
    public float tickTime;
    List<Sensor> sensors = new List<Sensor>(); 

    void Awake()
    {
        sensors.Add(new GPS_Sensor((float dt) => { return Vector3.zero; }, transform));
        InvokeRepeating("TestTick", tickTime, tickTime);
    }

    void TestTick()
    {
        SensorTick(tickTime);
    }

    public void SensorTick(float deltaTime)
    {
        if (sensors == null)
            return;

        for (int i = 0; i < sensors.Count; i++)
        {
            Debug.Log(sensors[i].Tick(deltaTime));
        }
    }
}

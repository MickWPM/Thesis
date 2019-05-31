using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GPS_Sensor : MonoBehaviour, Sensor
{
    [SerializeField] protected bool useMonoUpdate = true;
    [SerializeField] float updateTime = 0f; //Only needed if we arent using the mono update
    GPSData data;
    [SerializeField]
    Transform _positionTransform;
    public Transform PositionTransform { get => _positionTransform; protected set => _positionTransform = value; }
    public GPSData CurrentData { get => data; }

    Vector3 previousPosition = Vector3.zero;

    void Awake()
    {
        if (PositionTransform == null)
        {
            PositionTransform = transform;
        }
        previousPosition = PositionTransform.position;
    }

    float timeSinceLastUpdate = 0;


    void Update()
    {
        if (useMonoUpdate)
        {
            Tick(Time.deltaTime);
        } else
        {
            timeSinceLastUpdate += Time.deltaTime;
            if (timeSinceLastUpdate > updateTime)
            {
                Tick(timeSinceLastUpdate);
                timeSinceLastUpdate = 0;
            }
        }
    }

    public event System.Action<SensorData> GPSTickEvent;
    public SensorData Tick(float deltaTime)
    {
        //TODO: This might be better in fixed delta time calc?
        float speedKPH = 3.6f * (PositionTransform.position - previousPosition).magnitude / deltaTime;

        data = new GPSData(PositionTransform.position, speedKPH);
        
        GPSTickEvent?.Invoke(data);
        previousPosition = PositionTransform.position;
        return data;
    }
}

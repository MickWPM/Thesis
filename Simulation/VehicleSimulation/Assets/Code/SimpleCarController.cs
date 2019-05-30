using UnityEngine;
using System.Collections;
using System.Collections.Generic;

//Modified From:
//https://docs.unity3d.com/Manual/WheelColliderTutorial.html

[System.Serializable]
public class AxleInfo
{
    public WheelCollider leftWheel;
    public WheelCollider rightWheel;
    public Transform leftWheelModel;
    public Transform rightWheelModel;
    public bool motor;
    public bool steering;
}

public class SimpleCarController : MonoBehaviour
{
    public float velocity;

    public List<AxleInfo> axleInfos;
    public float maxMotorTorque;
    public float maxSteeringAngle;

    Rigidbody rb;
    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
        rb.centerOfMass = Vector3.up * 0.3f;
    }


    public void ApplyLocalPositionToVisuals(WheelCollider collider, Transform visualWheel)
    {
        if (visualWheel == null)
            return;

        Vector3 position;
        Quaternion rotation;
        collider.GetWorldPose(out position, out rotation);

        visualWheel.transform.position = position;
        visualWheel.transform.rotation = rotation;
    }

    
    public void FixedUpdate()
    {
        velocity = rb.velocity.magnitude * 3.6f;

        float motor = maxMotorTorque * Input.GetAxis("Vertical");
        float steering = maxSteeringAngle * Input.GetAxis("Horizontal");

        foreach (AxleInfo axleInfo in axleInfos)
        {
            if (axleInfo.steering)
            {
                axleInfo.leftWheel.steerAngle = steering;
                axleInfo.rightWheel.steerAngle = steering;
            }
            if (axleInfo.motor)
            {
                axleInfo.leftWheel.motorTorque = motor;
                axleInfo.rightWheel.motorTorque = motor;
            }
            ApplyLocalPositionToVisuals(axleInfo.leftWheel, axleInfo.leftWheelModel);
            ApplyLocalPositionToVisuals(axleInfo.rightWheel, axleInfo.rightWheelModel);
        }
    }
}
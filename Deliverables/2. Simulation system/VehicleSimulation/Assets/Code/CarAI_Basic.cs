using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarAI_Basic : MonoBehaviour
{
    public bool Active = false;
    public float maxAISpeed = 30;
    public NavigationSystem navigationSystem;
    public SimpleCarController carController;
    public KeyCode aiToggle = KeyCode.Space;

    private void Awake()
    {
        if (navigationSystem == null)
            navigationSystem = gameObject.GetComponentInChildren<NavigationSystem>();
        
        if (carController == null)
            carController = gameObject.GetComponentInChildren<SimpleCarController>();
    }

    void Update()
    {
        if (Input.GetKeyDown(aiToggle))
            Active = !Active;

        float motor, steer;
        if (!Active)
        {
            motor = Input.GetAxis("Vertical");
            steer = Input.GetAxis("Horizontal");
        } else
        {
            motor = navigationSystem.DistanceToNextWaypoint > 10 ? 1 : navigationSystem.DistanceToNextWaypoint / 10;
            if (carController.velocity > maxAISpeed)
                motor = 0;
            steer = navigationSystem.DirectionVectorToNextWaypoint.x;
        }

        carController.SetControlStatus(motor, steer);
    }
}

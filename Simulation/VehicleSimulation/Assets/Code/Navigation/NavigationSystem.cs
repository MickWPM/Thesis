using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NavigationSystem : MonoBehaviour
{
    public event System.Action<NavigationRoute> NavigationRouteCancelledEvent;
    public event System.Action<NavigationRoute> NavigationRouteSetEvent; //Doesnt throw new node focus event
    public event System.Action NavigationRouteCompleteEvent;
    public event System.Action<RoadNode> ArrivedAtNodeEvent;
    public event System.Action<RoadNode> NewNodeFocusEvent;  //Not thrown when a new route is set for first WP
    protected NavigationRoute _currentRoute;
    public NavigationRoute CurrentRoute
    {
        protected get
        {
            return _currentRoute;
        }
        set
        {
            if (!NavRouteActive)
                NavigationRouteCancelledEvent?.Invoke(_currentRoute);

            _currentRoute = value;
            NavigationRouteSetEvent?.Invoke(_currentRoute);
        }
    }

    Vector3 _directionVectorToNextWaypoint;
    float _distanceToNextWaypoint;
    public float DistanceToNextWaypoint { get => _distanceToNextWaypoint; }
    public Vector3 DirectionVectorToNextWaypoint { get => _directionVectorToNextWaypoint; }

    [SerializeField] protected GPS_Sensor gps;

    private void Awake()
    {
        if (gps == null)
            gps = gameObject.GetComponent<GPS_Sensor>();
        if (gps == null)
            gps = gameObject.GetComponentInChildren<GPS_Sensor>();
        if (gps == null)
        {
            Debug.LogError("NO GPS ON THIS OR CHILD OBJECTS", gameObject);
            this.enabled = false;
        }
    }

    private void Start()
    {
        gps.GPSTickEvent += OnGPSUpdate;
    }

    private void Update()
    {
        if (gps == null)
        {
            Debug.LogWarning("Navigation system does not have GPS");
            return;
        }

        //Do your own update stuff here

    }

    void OnGPSUpdate(SensorData sensorData)
    {
        GPSData data = (GPSData)sensorData;

        if (!NavRouteActive)
            return;

        Vector3 vectorToWP = VectorToNextWaypoint(true);
        _directionVectorToNextWaypoint = vectorToWP.normalized;
        _distanceToNextWaypoint = vectorToWP.magnitude;

        CheckArrivedAtNode();
    }

    public RoadNode GetCurrentWaypointRoadNode()
    {
        if (!NavRouteActive)
        {
            Debug.LogWarning("Attempted to get direction to next waypoint from empty waypoint list");
            return new RoadNode(Vector3.zero);
        }

        return CurrentRoute.waypoints[0];
    }

    Vector3 VectorToNextWaypoint(bool useGPSOrientation = false)
    {
        if (!NavRouteActive)
        {
            Debug.LogWarning("Attempted to get direction to next waypoint from empty waypoint list");
            return Vector3.zero;
        }
        if (useGPSOrientation)
        {
            return (gps.PositionTransform.InverseTransformPoint(CurrentRoute.waypoints[0].position));
        }
        return (CurrentRoute.waypoints[0].position - gps.PositionTransform.position);
    }

    [SerializeField] protected float waypointArriveDistance = 3f;
    void CheckArrivedAtNode()
    {
        if (DistanceToNextWaypoint > waypointArriveDistance)
            return;

        ArrivedAtNodeEvent?.Invoke(CurrentRoute.waypoints[0]);

        CurrentRoute.waypoints.RemoveAt(0);

        if (CurrentRoute.waypoints.Count == 0)
        {
            NavigationRouteCompleteEvent?.Invoke();
        } else
        {
            NewNodeFocusEvent?.Invoke(CurrentRoute.waypoints[0]);
        }
    }

    public bool NavRouteActive
    {
        get { return !(CurrentRoute.waypoints == null || CurrentRoute.waypoints.Count < 1); }
    }

    public override string ToString()
    {
        if (gps.CurrentData == null)
            return ("No GPS signal (DATA)");

        if (!NavRouteActive)
            return string.Format("Postition: {0}. No current route.", gps.CurrentData.position);

        string s = string.Format("Postition: {0}. Speed: {3} km/hr. Current waypoint: {1} / ({2} waypoints).", 
            gps.CurrentData.position, 
            GetCurrentWaypointRoadNode(), 
            CurrentRoute.waypoints.Count, 
            (int)(gps.CurrentData.speedKPH));

        s += string.Format("\nDistance: {0}m. Direction: {1}", DistanceToNextWaypoint, DirectionVectorToNextWaypoint);

        return s;
    }
}

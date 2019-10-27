using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class DebugUpdater : MonoBehaviour
{
    public UnityEngine.UI.Text debugText1;
    public NavigationSystem navigationSystem;
    public SimpleCarController carController;
    
    void Update()
    {
        debugText1.text = navigationSystem.ToString();
    }

    private void OnDrawGizmos()
    {
        if (!navigationSystem.NavRouteActive)
            return;

        Handles.color = Color.black;
        Handles.DrawAAPolyLine(8, carController.transform.position, navigationSystem.GetCurrentWaypointRoadNode().position);
    }
}

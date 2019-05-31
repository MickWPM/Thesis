using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class NodeVisualiser : MonoBehaviour
{
    public List<RoadNode> nodes = new List<RoadNode>();
    public Transform fromPos;

    public NavigationSystem navSystemToTest;

    private void Start()
    {
        nodes = GetNodesFromPos(fromPos.position);
        SetNavRoute();

        navSystemToTest.NavigationRouteCompleteEvent += SetNavRoute;
    }

    [ContextMenu("SetNavRoute")]
    public void SetNavRoute()
    {
        NavigationRoute navigationRoute = new NavigationRoute();
        navigationRoute.waypoints = GetAllNodes();
        navSystemToTest.CurrentRoute = navigationRoute;
    }

    private void OnDrawGizmos()
    {
        for (int i = 0; i < transform.childCount; i++)
        {
            Transform t = transform.GetChild(i);

            //TO IMPROVE
            //https://docs.unity3d.com/ScriptReference/Handles.Label.html
            Handles.Label(t.position, i.ToString());

            Gizmos.color = Color.black;
            Gizmos.DrawWireSphere(t.position, 2f);
        }
    }

    public List<RoadNode> GetNodesFromPos(Vector3 currentPos)
    {
        List<RoadNode> nodes = GetAllNodes();
        float minDist = float.MaxValue;
        int nodeIndex = -1;

        for (int i = 0; i < nodes.Count; i++)
        {
            float thisDist = Vector3.Distance(currentPos, nodes[i].position);
            if (thisDist > minDist)
                continue;

            minDist = thisDist;
            nodeIndex = i;
        }

        nodes.RemoveRange(0, nodeIndex);

        return nodes;
    }

    public List<RoadNode> GetAllNodes()
    {
        List<RoadNode> nodes = new List<RoadNode>(transform.childCount);
        Transform[] childTransforms = GetComponentsInChildren<Transform>();

        for (int i = 1; i < childTransforms.Length; i++)
        {
            nodes.Add(new RoadNode( transform.GetChild(i-1).position));
        }

        return nodes;
    }
}

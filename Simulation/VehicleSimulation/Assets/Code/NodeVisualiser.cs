using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class NodeVisualiser : MonoBehaviour
{
    public List<Vector3> nodes = new List<Vector3>();
    public Transform fromPos;

    private void Start()
    {
        nodes = GetNodesFromPos(fromPos.position);
    }

    private void OnDrawGizmosSelected()
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

    public List<Vector3> GetNodesFromPos(Vector3 currentPos)
    {
        List<Vector3> nodes = GetAllNodes();
        float minDist = float.MaxValue;
        int nodeIndex = -1;

        for (int i = 0; i < nodes.Count; i++)
        {
            float thisDist = Vector3.Distance(currentPos, nodes[i]);
            if (thisDist > minDist)
                continue;

            minDist = thisDist;
            nodeIndex = i;
        }

        nodes.RemoveRange(0, nodeIndex);

        return nodes;
    }

    public List<Vector3> GetAllNodes()
    {
        List<Vector3> nodes = new List<Vector3>(transform.childCount);
        Transform[] childTransforms = GetComponentsInChildren<Transform>();

        for (int i = 1; i < childTransforms.Length; i++)
        {
            nodes.Add(transform.GetChild(i-1).position);
        }

        return nodes;
    }
}

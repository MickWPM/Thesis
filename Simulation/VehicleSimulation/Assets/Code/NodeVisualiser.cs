using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

public class NodeVisualiser : MonoBehaviour
{
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
}

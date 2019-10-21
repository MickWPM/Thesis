using UnityEngine;

public struct RoadNode
{
    public Vector3 position;

    public RoadNode(Vector3 position)
    {
        this.position = position;
    }

    public override string ToString()
    {
        return position.ToString();
    }
}

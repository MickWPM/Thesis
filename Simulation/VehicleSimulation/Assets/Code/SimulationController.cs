using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SimulationController : MonoBehaviour
{
    public static SimulationController Instance;
    public event System.Action OnSimTickComplete;

    // Start is called before the first frame update
    void Awake()
    {
        Instance = this;
    }

    private void Start()
    {
        NextTick();
    }

    public float tickLength = 0.5f;
    public bool simulating = false;
    float thisSim;
    public float lastDeltaTime = 0.001f;
    bool started = false;

    void Update()
    {
        if (started == false)
        {
            if (Input.GetKeyDown(KeyCode.F))
            {
                started = true;
            }
        } else
        {
            lastDeltaTime = Time.deltaTime;
            if (nextTickTriggered)
            {
                NextTick();
            }

            if (!simulating)
                return;

            thisSim += Time.deltaTime;
            if (thisSim >= tickLength)
                SimTickDone();
        }

    }

    void SimTickDone()
    {
        Time.timeScale = 0;
        simulating = false;
        if (OnSimTickComplete != null)
            OnSimTickComplete();
    }

    bool nextTickTriggered = false;
    public void DoNextTick()
    {
        nextTickTriggered = true;
    }

    void NextTick()
    {
        nextTickTriggered = false;
        Time.timeScale = 1;
        thisSim = 0;
        simulating = true;
    }
}

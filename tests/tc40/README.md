# TC40: Small-screen and scalable text

Setup: Use the isolated services and exported applications in the [setup instructions](../../SETUP.md). Run these commands from this case folder. Device helpers require the debug APK, 1080 x 2400/density 420, 100% text, and the demo account unless the steps explicitly change them. Inspect screenshots after coordinate actions.

Procedure: Run existing 320 by 640 and 640 by 320 widget layouts at 100% and 200% text. Inspect estimate, profile, discovery and charging controls on Android.

Exact commands:

```powershell
python regression.py
python android-layout.py
```

Expected result: Required actions remain reachable without overflow or clipped financial figures. Record each viewport and scale.

Observed result: All 34 layout, typesetting and profile regression tests passed. Android portrait and landscape captures at 100% and 200% text show readable estimates and confirmation controls reachable by scrolling.

Status: Done.

Verdict: Passed.

Evidence:

- [requests.txt](requests.txt)
- [supplementary-regression.txt](supplementary-regression.txt)
- [1920x960-scale-1.0](1920x960-scale-1.0.png)
- [1920x960-scale-2.0](1920x960-scale-2.0.png)
- [960x1920-scale-1.0](960x1920-scale-1.0.png)
- [960x1920-scale-2.0](960x1920-scale-2.0.png)

- [Landscape estimate at 200% text](estimate-1920x960-scale-2.0.png)
- [Landscape confirmation controls after scrolling](estimate-1920x960-scale-2.0-scrolled.png)
- [Portrait estimate at 200% text](estimate-960x1920-scale-2.0.png)
- [Portrait confirmation controls after scrolling](estimate-960x1920-scale-2.0-scrolled.png)
- [Android layout commands](android-console.txt)

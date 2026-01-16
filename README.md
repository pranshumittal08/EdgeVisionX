# EdgeVisionX

## Project Overview

EdgeVisionX is an open-source framework for building and deploying computer vision workflows on edge devices (Raspberry Pi, NVIDIA Jetson, ARM SBCs, etc.). Inspired by canvas style visual workflow approach, EdgeVisionX allows developers to create hybrid CV pipelines by combining classical computer vision techniques with modern deep learning models, all automatically optimized for real-time inference on resource-constrained devices.

## Core Vision

Make edge computer vision deployment as simple as connecting nodes in a workflow - no more wrestling with PyTorch dependencies, ONNX conversions, or device-specific optimizations. Users focus on **what** they want to detect/track/analyze, EdgeCV handles **how** to run it efficiently on their device.

## Key Differentiators

1. **Workflow-Based Pipeline Builder**: Visual/code-based node graph for creating CV pipelines (detect → track → count → alert)
2. **Hybrid CV Approach**: Seamlessly combine classical CV (OpenCV operations) with modern DL models in single pipelines
3. **Automatic Edge Optimization**: Device detection, model quantization (PTQ), resolution selection, and thermal throttling - all automatic
4. **Deploy-First Philosophy**: ONNX Runtime backend (no PyTorch at runtime), <100MB install, works out-of-box on any edge device
5. **Pre-Built Pipeline Templates**: People counting, intrusion detection, quality inspection, pose estimation - production-ready in minutes

### Workflow Node Types

- **Input Nodes**: Camera, video file, image stream, RTSP
- **Preprocessing Nodes**: Resize, crop, denoise, color correction, ROI selection
- **Classical CV Nodes**: Edge detection, background subtraction, motion detection, morphology
- **Detection Nodes**: Object detection, segmentation, pose estimation, classification
- **Tracking Nodes**: SORT, ByteTrack, DeepSORT
- **Logic Nodes**: Zone/line crossing, dwell time, counting, filtering
- **Output Nodes**: Display, save, alert, API callback, database
import base64
import json
from typing import Any, Iterable, Optional
import numpy as np

try:
    import cv2
except ImportError:  # pragma: no cover
    cv2 = None

try:
    import mediapipe as mp
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False


def _to_bgr_image(image: Any):
    """Convert various image formats to OpenCV BGR format."""
    if isinstance(image, str):
        if ',' in image:
            _, data = image.split(',', 1)
        else:
            data = image
        try:
            raw = base64.b64decode(data, validate=False)
        except Exception:
            raw = data.encode('utf-8')
        if cv2 is not None:
            arr = np.frombuffer(raw, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is not None:
                return img
        return np.frombuffer(raw, dtype=np.uint8).reshape((-1, 1))

    if isinstance(image, np.ndarray):
        return image

    if hasattr(image, 'read'):
        image_bytes = image.read()
        if cv2 is not None:
            arr = np.frombuffer(image_bytes, dtype=np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            if img is not None:
                return img
        return np.frombuffer(image_bytes, dtype=np.uint8)

    raise ValueError('Unsupported image input type')


def compute_face_signature(image: Any):
    """Generate a robust face embedding using MediaPipe or OpenCV fallback."""
    frame = _to_bgr_image(image)

    if MEDIAPIPE_AVAILABLE and isinstance(frame, np.ndarray) and frame.ndim == 3:
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) if cv2 else frame
            with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
                results = detector.process(rgb_frame)
                if results.detections and len(results.detections) > 0:
                    detection = results.detections[0]
                    bbox = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x = max(0, int(bbox.xmin * w))
                    y = max(0, int(bbox.ymin * h))
                    x_max = min(w, int((bbox.xmin + bbox.width) * w))
                    y_max = min(h, int((bbox.ymin + bbox.height) * h))

                    roi = frame[y:y_max, x:x_max]
                    roi = cv2.resize(roi, (128, 128))
                    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    hist = cv2.calcHist([gray], [0], None, [64], [0, 256])
                    cv2.normalize(hist, hist)
                    signature = hist.flatten().tolist()
                    return [float(value) for value in signature]
                else:
                    raise ValueError('No face detected')
        except Exception:
            pass

    if cv2 is not None and isinstance(frame, np.ndarray) and frame.ndim == 3:
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if hasattr(cv2, 'CascadeClassifier'):
                cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                faces = cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=6)
                if len(faces) == 0:
                    raise ValueError('No face detected in the submitted image.')
                x, y, w, h = faces[0]
                roi = gray[y:y + h, x:x + w]
                roi = cv2.resize(roi, (128, 128))
                hist = cv2.calcHist([roi], [0], None, [64], [0, 256])
                cv2.normalize(hist, hist)
                signature = hist.flatten().tolist()
                return [float(value) for value in signature]
        except Exception:
            pass

    if isinstance(frame, np.ndarray):
        flat = frame.astype(np.float32).ravel()
        return [float(v) for v in flat[:256].tolist()]

    return [float(v) for v in np.asarray(frame).astype(float).tolist()]


def compare_face_signatures(stored_signature: Iterable[float], candidate_signature: Iterable[float]):
    """Return cosine similarity between two signatures in the range [0, 1]."""
    stored = np.asarray(stored_signature, dtype=np.float32)
    candidate = np.asarray(candidate_signature, dtype=np.float32)
    if stored.size == 0 or candidate.size == 0:
        return 0.0
    length = min(stored.size, candidate.size)
    stored = stored[:length]
    candidate = candidate[:length]
    denom = np.linalg.norm(stored) * np.linalg.norm(candidate)
    if denom == 0:
        return 0.0
    return float(np.dot(stored, candidate) / denom)


def verify_face_match(candidate_image: Any, stored_signature: Any, threshold: float = 0.78):
    """Check whether a captured image matches the stored signature."""
    if not stored_signature:
        return False
    try:
        candidate = compute_face_signature(candidate_image)
        similarity = compare_face_signatures(stored_signature, candidate)
        return similarity >= threshold
    except Exception:
        return False


def serialize_face_signature(signature):
    """JSON serialize a face signature."""
    return json.dumps(signature)


def deserialize_face_signature(value):
    """Deserialize a JSON face signature."""
    if not value:
        return None
    try:
        return json.loads(value)
    except Exception:
        return None

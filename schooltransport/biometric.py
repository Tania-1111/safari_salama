"""
Biometric System Module
Handles fingerprint and facial recognition verification
"""

try:
    import cv2
    _HAS_CV2 = True
except Exception:
    cv2 = None
    _HAS_CV2 = False
import numpy as np
from PIL import Image
import io
import base64
from typing import Dict, Tuple, Optional
import json


class BiometricSystem:
    """
    Biometric verification system (fingerprint-only)
    """

    def __init__(self):
        """Initialize biometric system (fingerprint only). Fingerprint processor is
        created lazily to allow importing this module in environments where
        OpenCV isn't available during import (e.g. mismatched NumPy/OpenCV wheels).
        """
        self.biometric_type = 'fingerprint'
        self.fingerprint_processor = None

    def enroll_biometric(self, image_data: str, student_name: str) -> Dict:
        """
        Enroll a new fingerprint sample

        Returns a dict with template or error.
        """
        try:
            image_array = self._decode_image(image_data)
            if self.fingerprint_processor is None:
                if not _HAS_CV2:
                    raise ImportError("OpenCV (cv2) is required for fingerprint enrollment. Install a compatible opencv-python and numpy.")
                self.fingerprint_processor = FingerprintProcessor()
            template = self.fingerprint_processor.create_template(image_array)
            return {
                'success': True,
                'template': template,
                'student_name': student_name,
                'biometric_type': self.biometric_type,
                'confidence': 95.0
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def verify_biometric(self, captured_data: str, stored_template: Dict) -> Tuple[bool, float]:
        """
        Verify captured fingerprint against stored template
        """
        try:
            captured_array = self._decode_image(captured_data)
            if self.fingerprint_processor is None:
                if not _HAS_CV2:
                    raise ImportError("OpenCV (cv2) is required for fingerprint verification. Install a compatible opencv-python and numpy.")
                self.fingerprint_processor = FingerprintProcessor()
            is_match, score = self.fingerprint_processor.match(captured_array, stored_template)
            return is_match, score
        except Exception as e:
            print(f"Verification error: {e}")
            return False, 0.0

    @staticmethod
    def _decode_image(image_data: str) -> np.ndarray:
        """Decode base64 image to numpy array"""
        try:
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]

            # Decode base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        except Exception as e:
            raise ValueError(f"Failed to decode image: {e}")


class FingerprintProcessor:
    """
    Fingerprint recognition using image processing
    In production, use libraries like: py-fingerprint, fingerprint-recognition
    """

    def __init__(self):
        # feature detector kept for fallback/hybrid matching
        self.orb = cv2.ORB_create(nfeatures=500)

    def create_template(self, image: np.ndarray) -> Dict:
        """
        Create fingerprint template from image
        
        Uses ORB (Oriented FAST and Rotated BRIEF) feature detector
        """
        processed = self._preprocess(image)

        # Binarize using adaptive threshold
        try:
            thresh = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY_INV, 11, 2)
        except Exception:
            # fallback to Otsu
            _, thresh = cv2.threshold(processed, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Convert to boolean image for skeletonize
        bin_img = (thresh > 0).astype(np.uint8)

        # Thinning / skeletonization using skimage
        from skimage.morphology import skeletonize
        skeleton = skeletonize(bin_img // 1)

        # Extract minutiae from skeleton
        minutiae = self._extract_minutiae(skeleton)

        if not minutiae:
            raise ValueError("No minutiae detected in fingerprint image")

        template = {
            'minutiae': minutiae,
            'image_hash': self._hash_image(processed)
        }

        return template

    def match(self, captured: np.ndarray, template: Dict) -> Tuple[bool, float]:
        """
        Match captured fingerprint with template
        """
        # Preprocess and extract minutiae from captured image
        processed = self._preprocess(captured)

        try:
            from skimage.morphology import skeletonize
            _, thresh = cv2.threshold(processed, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            bin_img = (thresh > 0).astype(np.uint8)
            skeleton = skeletonize(bin_img // 1)
            captured_minutiae = self._extract_minutiae(skeleton)
        except Exception as e:
            # Fallback: try ORB matching if skeletonization fails
            keypoints, descriptors = self.orb.detectAndCompute(processed, None)
            if descriptors is None or 'minutiae' not in template:
                return False, 0.0
            # No robust fallback scoring here; return low confidence
            return False, 10.0

        stored_minutiae = template.get('minutiae', [])

        if not stored_minutiae or not captured_minutiae:
            return False, 0.0

        # Simple matching: count stored minutiae that have a nearby captured minutia
        match_count = 0
        tolerance_px = 12  # matching distance tolerance

        used = [False] * len(captured_minutiae)

        for s in stored_minutiae:
            sx, sy, stype = s['x'], s['y'], s['type']
            for i, c in enumerate(captured_minutiae):
                if used[i]:
                    continue
                cx, cy, ctype = c['x'], c['y'], c['type']
                dist = np.hypot(sx - cx, sy - cy)
                if dist <= tolerance_px and stype == ctype:
                    match_count += 1
                    used[i] = True
                    break

        # Compute confidence relative to average number of minutiae
        denom = max(1, (len(stored_minutiae) + len(captured_minutiae)) / 2)
        confidence = min(100.0, (match_count / denom) * 100.0)
        is_match = confidence >= 60.0

        return is_match, confidence

    @staticmethod
    def _preprocess(image: np.ndarray) -> np.ndarray:
        """Preprocess fingerprint image"""
        # Apply histogram equalization
        equalized = cv2.equalizeHist(image)

        # Apply morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        morph = cv2.morphologyEx(equalized, cv2.MORPH_CLOSE, kernel)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(morph, (5, 5), 0)

        return blurred

    @staticmethod
    def _extract_minutiae(skeleton: np.ndarray) -> list:
        """Extract minutiae points (ridge endings and bifurcations) from a skeletonized image.

        Returns a list of dicts: { 'x': int, 'y': int, 'type': 'ending'|'bifurcation' }
        """
        minutiae = []
        # pad to avoid border issues
        img = (skeleton > 0).astype(np.uint8)
        h, w = img.shape

        # Neighbor offsets in clockwise order
        neigh = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

        for y in range(1, h - 1):
            for x in range(1, w - 1):
                if img[y, x] == 0:
                    continue

                # collect neighbors' binary values
                P = [img[y + dy, x + dx] for dy, dx in neigh]

                # crossing number
                cn = 0
                for i in range(len(P)):
                    cn += abs(P[i] - P[(i + 1) % len(P)])
                cn = cn / 2

                # Ridge ending: CN == 1, bifurcation: CN == 3
                if cn == 1:
                    minutiae.append({'x': int(x), 'y': int(y), 'type': 'ending'})
                elif cn == 3:
                    minutiae.append({'x': int(x), 'y': int(y), 'type': 'bifurcation'})

        return minutiae

    @staticmethod
    def _hash_image(image: np.ndarray) -> str:
        """Create hash of image for quick comparison"""
        import hashlib
        return hashlib.md5(image.tobytes()).hexdigest()


# Facial recognition support removed — this module now implements fingerprint-only


class BiometricDevice:
    """
    Interface for biometric input devices
    Supports webcam, fingerprint scanner, etc.
    """

    @staticmethod
    def capture_from_webcam(device_index=0, timeout=5000) -> Optional[str]:
        """
        Capture biometric from webcam
        
        Args:
            device_index: Camera device index
            timeout: Timeout in milliseconds
            
        Returns:
            Base64 encoded image or None
        """
        cap = cv2.VideoCapture(device_index)

        if not cap.isOpened():
            print("Failed to open camera")
            return None

        ret, frame = cap.read()
        cap.release()

        if ret:
            # Encode image to base64
            ret_encode, buffer = cv2.imencode('.jpg', frame)
            if ret_encode:
                image_base64 = base64.b64encode(buffer).decode('utf-8')
                return f"data:image/jpeg;base64,{image_base64}"

        return None

    @staticmethod
    def display_capture_preview(timeout=5000):
        """Display camera preview for capture"""
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Display frame
            cv2.imshow('Capture Biometric (Press SPACE to capture, Q to quit)', frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord(' '):  # Space to capture
                cap.release()
                cv2.destroyAllWindows()
                ret_encode, buffer = cv2.imencode('.jpg', frame)
                if ret_encode:
                    image_base64 = base64.b64encode(buffer).decode('utf-8')
                    return f"data:image/jpeg;base64,{image_base64}"

            elif key == ord('q'):  # Q to quit
                break

        cap.release()
        cv2.destroyAllWindows()
        return None


# Example usage and testing
if __name__ == "__main__":
    # Initialize fingerprint system
    biometric = BiometricSystem()

    # In a real application, this would come from camera input
    # For now, we'll demonstrate the API

    print("Biometric System initialized")
    print(f"Biometric Type: {biometric.biometric_type}")

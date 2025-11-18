import os
import sys

# Ensure workspace root is on path
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

import ezdxf
from bridge_processor import BridgeProcessor


def run_synthetic_cleanup_test():
    print("[Synthetic] Building test DXF with degenerate entities...")
    doc = ezdxf.new("R2010", setup=True)
    msp = doc.modelspace()

    # Add orphan/degenerate entities
    msp.add_point((0, 0))  # orphan POINT
    msp.add_line((1, 1), (1, 1))  # zero-length LINE
    # Degenerate LWPOLYLINE (zero extent)
    msp.add_lwpolyline([(2.0, 2.0), (2.0, 2.0)], format='xy', close=True)

    bp = BridgeProcessor()
    stats = bp.remove_orphan_points_and_degenerate_entities(doc)
    print("[Synthetic] Cleanup stats:", stats)

    # Basic assertions
    assert stats['points_removed'] >= 1, "Expected at least 1 POINT removed"
    assert stats['lines_removed'] >= 1, "Expected at least 1 LINE removed"
    assert stats['polylines_removed'] >= 1, "Expected at least 1 LWPOLYLINE removed"


def run_real_processing_test():
    print("[Real] Running processor on sample Excel...")
    sample_path = os.path.abspath(os.path.join(WORKSPACE_ROOT, 'attached_assets', 'input_1754197697460.xlsx'))
    if not os.path.exists(sample_path):
        raise FileNotFoundError(f"Sample Excel not found at {sample_path}")

    bp = BridgeProcessor()
    result = bp.process_excel_file(sample_path, project_name="TEST PROJECT")
    if not result.get('success'):
        raise RuntimeError(f"Processing failed: {result.get('error')}")

    print("[Real] Generated:", result.get('dxf_filename'))
    print("[Real] Cleanup stats:", result.get('cleanup'))


if __name__ == '__main__':
    run_synthetic_cleanup_test()
    run_real_processing_test()
    print("All tests passed.")
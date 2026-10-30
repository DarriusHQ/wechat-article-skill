# -*- coding: utf-8 -*-
"""
wechat-article · MIT License · Author: Darrius · https://github.com/DarriusHQ/wechat-article-skill

截图裁剪工具：裁掉截图边缘的内部术语面板/导航/空白，输出新文件。
依赖 Pillow（pip install pillow）。

用法：
  # 四边裁剪（坐标为保留区域的左/上/右/下像素）
  python3 crop_image.py 输入.png --left 230 --top 55 --right 1580 --bottom 869 -o 输出.png

  # 只裁掉底部 N 像素（常用：去底部操作条/空白）
  python3 crop_image.py 输入.png --trim-bottom 60 -o 输出.png

  # 只裁掉左侧 N 像素（常用：去导航栏）
  python3 crop_image.py 输入.png --trim-left 230 -o 输出.png
"""

import argparse
import sys

try:
    from PIL import Image
except ImportError:
    print("缺少 Pillow，请先安装：pip install pillow")
    sys.exit(2)


def main() -> int:
    ap = argparse.ArgumentParser(description="截图裁剪")
    ap.add_argument("input", help="输入图片路径")
    ap.add_argument("-o", "--output", help="输出路径（默认：<输入名>_裁剪.png）")
    ap.add_argument("--left", type=int, default=None, help="保留区域左边界（像素）")
    ap.add_argument("--top", type=int, default=None, help="保留区域上边界（像素）")
    ap.add_argument("--right", type=int, default=None, help="保留区域右边界（像素）")
    ap.add_argument("--bottom", type=int, default=None, help="保留区域下边界（像素）")
    ap.add_argument("--trim-left", type=int, default=0, help="裁掉左侧 N 像素")
    ap.add_argument("--trim-top", type=int, default=0, help="裁掉顶部 N 像素")
    ap.add_argument("--trim-right", type=int, default=0, help="裁掉右侧 N 像素")
    ap.add_argument("--trim-bottom", type=int, default=0, help="裁掉底部 N 像素")
    args = ap.parse_args()

    img = Image.open(args.input)
    w, h = img.size
    left = args.left if args.left is not None else args.trim_left
    top = args.top if args.top is not None else args.trim_top
    right = args.right if args.right is not None else w - args.trim_right
    bottom = args.bottom if args.bottom is not None else h - args.trim_bottom

    if not (0 <= left < right <= w and 0 <= top < bottom <= h):
        print(f"错误：裁剪区域无效 (left={left}, top={top}, right={right}, bottom={bottom})，"
              f"图片尺寸 {w}x{h}")
        return 2

    out = img.crop((left, top, right, bottom))
    import pathlib
    out_path = args.output or str(pathlib.Path(args.input).with_name(
        pathlib.Path(args.input).stem + "_裁剪.png"))
    out.save(out_path)
    print(f"✓ 已输出 {out_path}（{out.size[0]}x{out.size[1]}，原图 {w}x{h}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())

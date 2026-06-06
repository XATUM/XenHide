# Maintainer: Xenon Akro <xenonakro@gmail.com>
pkgname=xenhide
pkgver=1.0
pkgrel=1
pkgdesc="A steganography tool to hide and reveal secret messages inside images"
arch=("x86_64")
url="https://codeberg.org/metrinaveen08/XenHide"
license=('GPL3')
depends=('python' 'python-pyqt5' 'python-pillow' 'python-pip')
options=(!strip)
source=("$pkgname-$pkgver.tar.gz::https://codeberg.org/metrinaveen08/XenHide/archive/v${pkgver}.tar.gz")
sha256sums=('SKIP')

package() {
    cd "$srcdir/xenhide"
   pip install stegano piexif opencv-python-headless --target "$pkgdir/usr/lib/xenhide/libs" --quiet
rm -rf "$pkgdir/usr/lib/xenhide/libs/PIL"
rm -rf "$pkgdir/usr/lib/xenhide/libs/Pillow"*
rm -rf "$pkgdir/usr/lib/xenhide/libs/cv2/qt"

    install -Dm644 xencrypt.py "$pkgdir/usr/lib/xenhide/xencrypt.py"
    install -Dm644 xendcrypt.py "$pkgdir/usr/lib/xenhide/xendcrypt.py"
    install -Dm644 Application/XenHideGUI.py "$pkgdir/usr/lib/xenhide/XenHideGUI.py"
    install -Dm644 Assets/logo.png "$pkgdir/usr/share/pixmaps/xenhide.png"

    install -dm755 "$pkgdir/usr/bin"
 cat > "$pkgdir/usr/bin/xenhide" << 'EOF'
#!/bin/sh
export QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins
export OPENCV_IO_ENABLE_OPENEXR=0
export PYTHONPATH=/usr/lib/xenhide:/usr/lib/xenhide/libs
python -c "
import sys, os, runpy
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = '/usr/lib/qt/plugins'
sys.path.insert(0, '/usr/lib/xenhide')
sys.path.insert(1, '/usr/lib/xenhide/libs')
runpy.run_path('/usr/lib/xenhide/XenHideGUI.py', run_name='__main__')
" "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/xenhide"

    install -dm755 "$pkgdir/usr/share/applications"
    cat > "$pkgdir/usr/share/applications/xenhide.desktop" << EOF
[Desktop Entry]
Name=XenHide
Comment=Steganography tool to hide messages inside images
Exec=env QT_QPA_PLATFORM=xcb QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/qt/plugins /usr/bin/xenhide
Icon=/usr/share/pixmaps/xenhide.png
Terminal=false
Type=Application
Categories=Security;Education;
EOF
}
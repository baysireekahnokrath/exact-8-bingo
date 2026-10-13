// Leather cube: 6 pieces of pattern 05 (circle D90). Tab-through-slit joints. Units: mm. Three.js r128.
(function () {
  const R = 45, H = R / Math.SQRT2, T = 1.4;           // circle radius, half fold square, thickness
  const UP = new THREE.Vector3(0, 1, 0);
  const COLORS = { y: 0x8f5228, x: 0xc48a52, z: 0x4a2f1d };

  let grain = null; const cache = {};
  function grainTexture() {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const x = c.getContext('2d'), img = x.createImageData(256, 256);
    for (let i = 0; i < img.data.length; i += 4) {
      const v = 215 + Math.random() * 40; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(0.05, 0.05); return t;
  }
  function mats(color) {
    if (!grain) grain = grainTexture();
    if (!cache[color]) cache[color] = [
      new THREE.MeshStandardMaterial({ color, map: grain, bumpMap: grain, bumpScale: 0.25, roughness: 0.78, side: THREE.DoubleSide }),
      new THREE.MeshStandardMaterial({ color: new THREE.Color(color).multiplyScalar(0.55), roughness: 0.6, side: THREE.DoubleSide })];
    return cache[color];
  }
  function capShape() {
    const sh = new THREE.Shape(), N = 36;
    sh.moveTo(-H, 0);
    for (let i = 0; i <= N; i++) { const s = -H + 2 * H * i / N; sh.lineTo(s, Math.max(Math.sqrt(R * R - s * s) - H, 0)); }
    sh.lineTo(H, 0); sh.closePath(); return sh;
  }
  function addCap(group, color, origin, sA, dA, nA, offset) {
    const g = new THREE.ExtrudeGeometry(capShape(), { depth: T, bevelEnabled: false, curveSegments: 4 });
    const m = new THREE.Matrix4().makeBasis(sA, dA, nA); m.setPosition(origin.clone().addScaledVector(nA, offset));
    g.applyMatrix4(m);
    const mesh = new THREE.Mesh(g, mats(color)); mesh.castShadow = mesh.receiveShadow = true; group.add(mesh);
  }
  const axisOf = v => Math.abs(v.x) > 0.5 ? 'x' : Math.abs(v.y) > 0.5 ? 'y' : 'z';
  // face on axis X sends tabs (A) toward Y, Y toward Z, Z toward X; the other pair receives (B)
  const isTab = (f, nb) => ({ x: 'y', y: 'z', z: 'x' })[f] === nb;

  // state: {fold, corners, lid: 'none'|'above'|'closed', lidLift}
  function build(state) {
    const th = THREE.MathUtils.degToRad(state.fold), group = new THREE.Group();
    const dirs = [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 1), new THREE.Vector3(-1, 0, 0), new THREE.Vector3(0, 0, -1)];
    const base = { c: new THREE.Vector3(), a: new THREE.Vector3(1, 0, 0), b: new THREE.Vector3(0, 0, 1), n: new THREE.Vector3(0, -1, 0), logical: new THREE.Vector3(0, -1, 0) };
    const walls = dirs.map(d => {
      const u = d.clone().multiplyScalar(Math.cos(th)).addScaledVector(UP, Math.sin(th));
      const n = d.clone().multiplyScalar(Math.sin(th)).addScaledVector(UP, -Math.cos(th));
      return { c: d.clone().multiplyScalar(H).addScaledVector(u, H), a: new THREE.Vector3().crossVectors(u, n), b: u, n, d, logical: d };
    });
    const faces = [base, ...walls];
    let lid = null;
    if (state.lid !== 'none') {
      lid = { c: new THREE.Vector3(0, 2 * H + (state.lid === 'above' ? state.lidLift : 0), 0), a: new THREE.Vector3(0, 0, 1),
              b: new THREE.Vector3(1, 0, 0), n: UP.clone(), logical: UP.clone() };
      faces.push(lid);
    }
    faces.forEach(f => { f.color = COLORS[axisOf(f.logical)]; });
    const seam = new Map();
    dirs.forEach((d, k) => { seam.set(`0:${k}`, k + 1); seam.set(`${k + 1}:3`, 0); });
    if (state.corners) walls.forEach((w, k) => {
      const a90 = new THREE.Vector3().crossVectors(UP, w.d);
      dirs.forEach((d2, j) => { if (d2.dot(a90) > 0.9) seam.set(`${k + 1}:0`, j + 1); if (d2.dot(a90) < -0.9) seam.set(`${k + 1}:2`, j + 1); });
    });
    if (lid && state.lid === 'closed') {
      const li = faces.length - 1;
      walls.forEach((w, k) => seam.set(`${k + 1}:1`, li));
      [lid.a, lid.b, lid.a.clone().negate(), lid.b.clone().negate()].forEach((dv, k) =>
        dirs.forEach((d2, j) => { if (d2.dot(dv) > 0.9) seam.set(`${li}:${k}`, j + 1); }));
    }
    faces.forEach((f, i) => {
      const [fm, em] = mats(f.color);
      const slab = new THREE.Mesh(new THREE.BoxGeometry(2 * H, 2 * H, T), [em, em, em, em, fm, fm]);
      slab.applyMatrix4(new THREE.Matrix4().makeBasis(f.a, f.b, f.n).setPosition(f.c));
      slab.castShadow = slab.receiveShadow = true; group.add(slab);
      const dirsF = [f.a, f.b, f.a.clone().negate(), f.b.clone().negate()];
      const tans = [f.b.clone().negate(), f.a, f.b, f.a.clone().negate()];
      for (let k = 0; k < 4; k++) {
        const dir = dirsF[k], mid = f.c.clone().addScaledVector(dir, H), nb = seam.get(`${i}:${k}`);
        if (nb !== undefined) {
          const g = faces[nb], dA = g.c.clone().sub(mid).normalize();
          const tab = isTab(axisOf(f.logical), axisOf(g.logical));
          addCap(group, f.color, mid, tans[k], dA, g.n, tab ? -T / 2 - T - 0.05 : T / 2 + 0.05);   // tab inside, receiver flap outside
        } else {
          const psi = THREE.MathUtils.degToRad(f === lid ? -65 : 0);
          const dA = dir.clone().multiplyScalar(Math.cos(psi)).addScaledVector(f.n, Math.sin(psi));
          const nA = f.n.clone().multiplyScalar(Math.cos(psi)).addScaledVector(dir, -Math.sin(psi));
          addCap(group, f.color, mid, tans[k], dA, nA, -T / 2);
        }
      }
    });
    return group;
  }

  function makeScene(state) {
    const scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xfff6ec, 0x6b5a4c, 0.75));
    const key = new THREE.DirectionalLight(0xffffff, 0.95);
    key.position.set(-80, 190, 120); key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -150, right: 150, top: 150, bottom: -150, near: 10, far: 500 });
    scene.add(key);
    const fill = new THREE.DirectionalLight(0xffe2c4, 0.3); fill.position.set(140, 70, -70); scene.add(fill);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), new THREE.ShadowMaterial({ opacity: 0.16 }));
    ground.rotation.x = -Math.PI / 2; ground.position.y = -2.4; ground.receiveShadow = true; scene.add(ground);
    scene.add(build(state)); return scene;
  }
  window.LeatherCube = { makeScene, H };
})();

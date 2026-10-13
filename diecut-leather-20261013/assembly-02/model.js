// Petal cube: 5 pieces of pattern 02 woven into an open box. Units: mm. Three.js r128 globals.
(function () {
  const H = 27, T = 1.4, R = 29.25, C = 11.25;           // half face, leather thickness, lobe circle
  const UP = new THREE.Vector3(0, 1, 0);
  const COLORS = { base: 0x8f5228, light: 0xc48a52, dark: 0x4a2f1d };

  function grainTexture() {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const x = c.getContext('2d'), img = x.createImageData(256, 256);
    for (let i = 0; i < img.data.length; i += 4) {
      const v = 215 + Math.random() * 40;
      img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255;
    }
    x.putImageData(img, 0, 0);
    const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(0.05, 0.05);
    return t;
  }
  let grain = null;
  const matCache = {};
  // [grain face, burnished cut edge]
  function mats(color) {
    if (!grain) grain = grainTexture();
    if (!matCache[color]) {
      const face = new THREE.MeshStandardMaterial({
        color, map: grain, bumpMap: grain, bumpScale: 0.25, roughness: 0.78, metalness: 0, side: THREE.DoubleSide });
      const edge = new THREE.MeshStandardMaterial({
        color: new THREE.Color(color).multiplyScalar(0.55), roughness: 0.6, side: THREE.DoubleSide });
      matCache[color] = [face, edge];
    }
    return matCache[color];
  }

  function capShape(s0, s1) {
    const sh = new THREE.Shape(), N = 28;
    sh.moveTo(s0, 0);
    for (let i = 0; i <= N; i++) {
      const s = s0 + (s1 - s0) * i / N;
      sh.lineTo(s, Math.max(Math.sqrt(R * R - s * s) - C, 0));
    }
    sh.lineTo(s1, 0); sh.closePath();
    return sh;
  }

  function place(geo, origin, sA, dA, nA, offset) {
    const m = new THREE.Matrix4().makeBasis(sA, dA, nA);
    m.setPosition(origin.clone().addScaledVector(nA, offset));
    geo.applyMatrix4(m); return geo;
  }

  function addCap(group, color, s0, s1, origin, sA, dA, nA, offset) {
    const g = new THREE.ExtrudeGeometry(capShape(s0, s1), { depth: T, bevelEnabled: false, curveSegments: 4 });
    const mesh = new THREE.Mesh(place(g, origin, sA, dA, nA, offset), mats(color));
    mesh.castShadow = mesh.receiveShadow = true; group.add(mesh);
  }

  // face = {c, a, b, n, color}; a x b = n, n points out of the box (grain side)
  function edgeInfo(f, k) {
    const dir = [f.a, f.b, f.a.clone().negate(), f.b.clone().negate()][k];
    const t = [f.b.clone().negate(), f.a, f.b, f.a.clone().negate()][k]; // clockwise seen from outside
    return { dir, t, mid: f.c.clone().addScaledVector(dir, H) };
  }

  function build(state) {
    const th = THREE.MathUtils.degToRad(state.fold);
    const group = new THREE.Group();
    const base = { c: new THREE.Vector3(0, 0, 0), a: new THREE.Vector3(1, 0, 0), b: new THREE.Vector3(0, 0, 1),
                   n: new THREE.Vector3(0, -1, 0), color: COLORS.base };
    const dirs = [new THREE.Vector3(1, 0, 0), new THREE.Vector3(0, 0, 1), new THREE.Vector3(-1, 0, 0), new THREE.Vector3(0, 0, -1)];
    const walls = dirs.map((d, k) => {
      const u = d.clone().multiplyScalar(Math.cos(th)).addScaledVector(UP, Math.sin(th));
      const n = d.clone().multiplyScalar(Math.sin(th)).addScaledVector(UP, -Math.cos(th));
      const c = d.clone().multiplyScalar(H).addScaledVector(u, H);
      return { c, a: new THREE.Vector3().crossVectors(u, n), b: u, n, color: k % 2 ? COLORS.dark : COLORS.light, d };
    });
    const faces = [base, ...walls];
    // seams: face index, edge -> neighbour face index
    const seam = new Map();
    dirs.forEach((d, k) => { seam.set(`0:${k}`, k + 1); seam.set(`${k + 1}:3`, 0); });
    if (state.corners) {
      walls.forEach((w, k) => {
        const a90 = new THREE.Vector3().crossVectors(UP, w.d);
        dirs.forEach((d2, j) => {
          if (d2.dot(a90) > 0.9) { seam.set(`${k + 1}:0`, j + 1); }
          if (d2.dot(a90) < -0.9) { seam.set(`${k + 1}:2`, j + 1); }
        });
      });
    }
    faces.forEach((f, i) => {
      const [fm, em] = mats(f.color);
      const slab = new THREE.Mesh(new THREE.BoxGeometry(2 * H, 2 * H, T), [em, em, em, em, fm, fm]);
      slab.applyMatrix4(new THREE.Matrix4().makeBasis(f.a, f.b, f.n).setPosition(f.c));
      slab.castShadow = slab.receiveShadow = true; group.add(slab);
      for (let k = 0; k < 4; k++) {
        const e = edgeInfo(f, k), nb = seam.get(`${i}:${k}`);
        if (nb !== undefined) {
          const g = faces[nb], dA = g.c.clone().sub(e.mid).normalize();
          const eps = 0.04 * (i + 1);
          addCap(group, f.color, -H, 0, e.mid, e.t, dA, g.n, -T / 2 - T - eps);   // free half: under
          addCap(group, f.color, 0, H, e.mid, e.t, dA, g.n, T / 2 + eps);         // hinged half: over
        } else {
          const psi = THREE.MathUtils.degToRad(k === 1 && i > 0 ? state.flare : 0);
          const dA = e.dir.clone().multiplyScalar(Math.cos(psi)).addScaledVector(f.n, Math.sin(psi));
          const nA = f.n.clone().multiplyScalar(Math.cos(psi)).addScaledVector(e.dir, -Math.sin(psi));
          addCap(group, f.color, -H, H, e.mid, e.t, dA, nA, -T / 2);
        }
      }
    });
    if (state.plant) group.add(plant());
    return group;
  }

  function plant() {
    const g = new THREE.Group();
    const soil = new THREE.Mesh(new THREE.CylinderGeometry(23, 23, 2, 40),
      new THREE.MeshStandardMaterial({ color: 0x3b2a1e, roughness: 1 }));
    soil.position.y = 47; g.add(soil);
    const leafMat = new THREE.MeshStandardMaterial({ color: 0x47794a, roughness: 0.5 });
    const rings = [[10, 16, 70, 1.25], [8, 9, 52, 1.0], [5, 3, 30, 0.75]];
    rings.forEach(([n, r, tilt, s], ri) => {
      for (let i = 0; i < n; i++) {
        const leaf = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), leafMat);
        leaf.scale.set(4.2 * s, 2.2 * s, 10 * s);
        const a = (i / n) * Math.PI * 2 + ri * 0.4;
        const pivot = new THREE.Group(); pivot.rotation.y = a; pivot.position.y = 52 + ri * 2;
        leaf.position.set(0, 0, r * 0.5 + 6 * s); leaf.rotation.x = -THREE.MathUtils.degToRad(90 - tilt);
        leaf.castShadow = true; pivot.add(leaf); g.add(pivot);
      }
    });
    return g;
  }

  function makeScene(state) {
    const scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xfff6ec, 0x6b5a4c, 0.75));
    const key = new THREE.DirectionalLight(0xffffff, 0.95);
    key.position.set(-70, 160, 110); key.castShadow = true;
    key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -120, right: 120, top: 120, bottom: -120, near: 10, far: 400 });
    scene.add(key);
    const fill = new THREE.DirectionalLight(0xffe2c4, 0.3); fill.position.set(120, 60, -60); scene.add(fill);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), new THREE.ShadowMaterial({ opacity: 0.16 }));
    ground.rotation.x = -Math.PI / 2; ground.position.y = -2.4; ground.receiveShadow = true; scene.add(ground);
    scene.add(build(state));
    return scene;
  }

  window.PetalCube = { makeScene };
})();

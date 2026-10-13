// Bear charm: pattern 01 + heart strap 01-S hanging from a key ring. Units: mm. Three.js r128.
(function () {
  const D = __DATA__;
  const TB = 2.0, TS = 1.3;                        // bear / strap leather thickness
  const OX = 47.5, OY = 45;                        // CAD -> scene offset
  const Z_BACK = -(TB / 2 + TS / 2), Z_FRONT = TB / 2 + TS / 2;
  const YB = 98 - OY;                              // top of the strap loop (ring bar)
  const RING_R = 11, RING_T = 1.3, U_R = RING_T + TS / 2;
  const COL = { bear: 0xc48a52, strap: 0xb8434f, ring: 0xc9ccd1 };
  const v2 = p => new THREE.Vector2(p[0] - OX, p[1] - OY);

  let grain = null; const cache = {};
  function grainTexture() {
    const c = document.createElement('canvas'); c.width = c.height = 256;
    const x = c.getContext('2d'), img = x.createImageData(256, 256);
    for (let i = 0; i < img.data.length; i += 4) { const v = 215 + Math.random() * 40; img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
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
  function mesh(geo, m) { const o = new THREE.Mesh(geo, m); o.castShadow = o.receiveShadow = true; return o; }

  function bearMesh() {
    const sh = new THREE.Shape(D.outline.map(v2));
    const g = new THREE.ExtrudeGeometry(sh, { depth: TB, bevelEnabled: false, curveSegments: 6 });
    g.translate(0, 0, -TB / 2);
    const grp = new THREE.Group(); grp.add(mesh(g, mats(COL.bear)));
    const dark = new THREE.MeshBasicMaterial({ color: 0x3a2414 });
    D.slits.forEach(([a, b]) => {
      const A = v2(a), B = v2(b), len = A.distanceTo(B);
      const s = new THREE.Mesh(new THREE.PlaneGeometry(len, 0.5), dark);
      s.position.set((A.x + B.x) / 2, (A.y + B.y) / 2, TB / 2 + 0.02);
      s.rotation.z = Math.atan2(B.y - A.y, B.x - A.x); grp.add(s);
    });
    return grp;
  }

  // heart on the front: point hidden in the slit, lobes toward the face centre
  function heart(slit) {
    const S = v2(slit[0]).add(v2(slit[1])).multiplyScalar(0.5), C = v2(D.center);
    const u = C.clone().sub(S).normalize(), N = D.heart.neck;
    const g = new THREE.ExtrudeGeometry(new THREE.Shape(D.heart.pts.map(p => new THREE.Vector2(p[0], p[1]))),
      { depth: TS, bevelEnabled: false, curveSegments: 6 });
    // local x from the heart tip; world = S + (x - N) u + y v,  v = (-u.y, u.x)
    g.applyMatrix4(new THREE.Matrix4().set(
      u.x, -u.y, 0, S.x - N * u.x,
      u.y, u.x, 0, S.y - N * u.y,
      0, 0, 1, TB / 2,
      0, 0, 0, 1));
    return mesh(g, mats(COL.strap));
  }

  // flat ribbon along a path: centre points + width vectors
  function ribbon(P, Wv, w, t) {
    const pos = [], idx = [], n = P.length;
    for (let i = 0; i < n; i++) {
      const tan = P[Math.min(i + 1, n - 1)].clone().sub(P[Math.max(i - 1, 0)]).normalize();
      const nor = new THREE.Vector3().crossVectors(tan, Wv[i]).normalize();
      [[-1, -1], [1, -1], [1, 1], [-1, 1]].forEach(([a, b]) => {
        const p = P[i].clone().addScaledVector(Wv[i], a * w / 2).addScaledVector(nor, b * t / 2);
        pos.push(p.x, p.y, p.z);
      });
    }
    for (let i = 0; i < n - 1; i++) for (let k = 0; k < 4; k++) {
      const a = i * 4 + k, b = i * 4 + (k + 1) % 4, c = a + 4, d = b + 4;
      idx.push(a, b, d, a, d, c);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx); g.computeVertexNormals();
    return g;
  }

  function strap() {
    const Z = new THREE.Vector3(0, 0, 1);
    const mid = s => v2(s[0]).add(v2(s[1])).multiplyScalar(0.5);
    const SL = mid(D.slits[0]), SR = mid(D.slits[1]);
    const P = [], Wv = [];
    const twistStart = 84 - OY;
    function push(p, tan) {
      const flat = new THREE.Vector3().crossVectors(Z, tan).normalize();
      const f = THREE.MathUtils.clamp((p.y - twistStart) / (YB - twistStart), 0, 1);
      const phi = f * Math.PI / 2;
      P.push(p); Wv.push(flat.multiplyScalar(Math.cos(phi)).addScaledVector(Z, Math.sin(phi)).normalize());
    }
    const legA = new THREE.Vector3(SL.x, SL.y, Z_BACK), topA = new THREE.Vector3(-U_R, YB, Z_BACK);
    const legB = new THREE.Vector3(SR.x, SR.y, Z_BACK), topB = new THREE.Vector3(U_R, YB, Z_BACK);
    const tA = topA.clone().sub(legA).normalize();
    for (let i = 0; i <= 40; i++) push(legA.clone().lerp(topA, i / 40), tA);
    for (let i = 1; i < 24; i++) {                // over the ring bar
      const a = Math.PI - Math.PI * i / 24;
      const p = new THREE.Vector3(U_R * Math.cos(a), YB + U_R * Math.sin(a), Z_BACK);
      P.push(p); Wv.push(Z.clone());
    }
    const tB = legB.clone().sub(topB).normalize();
    for (let i = 0; i <= 40; i++) push(topB.clone().lerp(legB, i / 40), tB);
    const g = ribbon(P, Wv, D.heart.w, TS);
    return mesh(g, new THREE.MeshStandardMaterial({ color: COL.strap, roughness: 0.75, side: THREE.DoubleSide }));
  }

  function ring() {
    const g = new THREE.TorusGeometry(RING_R, RING_T, 16, 64);
    const m = mesh(g, new THREE.MeshStandardMaterial({ color: COL.ring, metalness: 0.85, roughness: 0.28 }));
    m.rotation.y = Math.PI / 2; m.position.set(0, YB + RING_R, Z_BACK); return m;
  }

  // view: 'front' | 'back'
  function makeScene(opts) {
    const scene = new THREE.Scene();
    scene.add(new THREE.HemisphereLight(0xfff6ec, 0x6b5a4c, 0.8));
    const key = new THREE.DirectionalLight(0xffffff, 0.9);
    key.position.set(-60, 120, 160); key.castShadow = true; key.shadow.mapSize.set(2048, 2048);
    Object.assign(key.shadow.camera, { left: -120, right: 120, top: 120, bottom: -120, near: 10, far: 500 });
    scene.add(key);
    const rim = new THREE.DirectionalLight(0xffe2c4, 0.35); rim.position.set(80, 40, -120); scene.add(rim);
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(800, 800), new THREE.ShadowMaterial({ opacity: 0.14 }));
    wall.position.z = opts.view === 'back' ? 45 : -45; wall.rotation.y = opts.view === 'back' ? Math.PI : 0;
    wall.receiveShadow = true; scene.add(wall);
    if (opts.view === 'back') { key.position.set(60, 120, -160); rim.position.set(-80, 40, 120); }
    const charm = new THREE.Group();
    charm.add(bearMesh(), heart(D.slits[0]), heart(D.slits[1]), strap(), ring());
    scene.add(charm);
    return scene;
  }
  window.BearCharm = { makeScene };
})();

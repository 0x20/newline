let scene, camera, renderer, benchy, arm, extruder;
// Benchy start and end  position, with rotations
const benchyRotationFix = { x: -Math.PI / 2, y: 0, z: -Math.PI / 2 }
const benchyStartPos = {
    x: 8, y: 5, z: -10,
    rotationX: benchyRotationFix.x + 1,
    rotationY: benchyRotationFix.y,
    rotationZ: benchyRotationFix.z - 1
};
const benchyEndPos = {
    x: -15, y: 0, z: -6,
    rotationX: benchyRotationFix.x + 0.5,
    rotationY: benchyRotationFix.y,
    rotationZ: benchyRotationFix.z + 0.7
};
// Bambu arm position
const armStartPos = { x: 1, y: -9, z: -1 };

// Red lines for background animation
const lineMaterial = new THREE.LineBasicMaterial({ color: 0x111111, linewidth: 0.1 });
const lines = [];

async function init() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5; // Set the camera position to ensure the model is visible
    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Add a light to illuminate the model
    const light = new THREE.PointLight(0xFFFFFF, 1);
    light.position.set(50, 50, 50); // Position the light
    scene.add(light);

    const loader = new THREE.STLLoader();

    await loader.load('./models/benchy.stl', function (geometry) {
        // Use MeshStandardMaterial for normal shading (shaded model)
        const material = new THREE.MeshStandardMaterial({ color: 0xEF1C2A, flatShading: true });

        // Create the mesh from geometry and apply material
        benchy = new THREE.Mesh(geometry, material);
        benchy.scale.set(0.1, 0.1, 0.1);  // Scale to appropriate size
        benchy.position.set(benchyStartPos.x, benchyStartPos.y, benchyStartPos.z);
        scene.add(benchy);

        onScroll();
    });

    loader.load('./models/rail with filament cutter.stl', function (geometry) {
        // Reset origin
        geometry.computeBoundingBox();
        const center = new THREE.Vector3();
        geometry.boundingBox.getCenter(center);
        geometry.translate(-center.x, -center.y, -center.z);

        const material = new THREE.MeshStandardMaterial({ color: 0xEF1C2A, flatShading: true });
        arm = new THREE.Mesh(geometry, material);
        const scale = 0.1;
        arm.scale.set(scale, scale, scale);
        arm.position.set(armStartPos.x, armStartPos.y, armStartPos.z);
        arm.rotation.x = - Math.PI / 2;
        arm.rotation.z = -Math.PI / 2;
        scene.add(arm);
        onScroll();
    });

    loader.load('./models/extruder.stl', function (geometry) {
        // Reset origin
        geometry.computeBoundingBox();
        const center = new THREE.Vector3();
        geometry.boundingBox.getCenter(center);
        geometry.translate(-center.x, -center.y, -center.z);

        const material = new THREE.MeshStandardMaterial({ color: 0xEF1C2A, flatShading: true });
        extruder = new THREE.Mesh(geometry, material);
        const scale = 0.1;
        extruder.scale.set(scale, scale, scale);
        extruder.position.set(0, armStartPos.y, armStartPos.z -0.15);
        extruder.rotation.x = - Math.PI / 2;
        extruder.rotation.z = -Math.PI / 2;
        scene.add(extruder);

    });

    // Create moving lines for background
    createBackgroundLines();
    window.addEventListener('scroll', onScroll);
    animate();
}

function createBackgroundLines() {
    for (let i = 0; i < 10; i++) {
        const points = [];
        for (let j = 0; j < 10; j++) {
            // Create random points for the lines to make it dynamic
            points.push(new THREE.Vector3(Math.random() * 200 - 100, Math.random() * 200 - 100, Math.random() * -500)); // Far away
        }
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const line = new THREE.Line(geometry, lineMaterial);
        lines.push(line);
        scene.add(line);
    }
}

function onScroll() {
    // Calculate the scroll progress 
    let scrollY = window.scrollY / window.innerHeight / 2;

    if (benchy) {
        let limitedScrollY = Math.min(scrollY, 1);

        // Move the boat along the 3D path from top-right to center-left
        benchy.position.x = benchyStartPos.x + (benchyEndPos.x - benchyStartPos.x) * limitedScrollY;
        benchy.position.y = benchyStartPos.y + (benchyEndPos.y - benchyStartPos.y) * limitedScrollY;
        benchy.position.z = benchyStartPos.z + (benchyEndPos.z - benchyStartPos.z) * limitedScrollY;

        // Rotate the boat based on scroll (from start rotation to end rotation)

        benchy.rotation.x = benchyStartPos.rotationX + (benchyEndPos.rotationX - benchyStartPos.rotationX) * limitedScrollY;
        benchy.rotation.y = benchyStartPos.rotationY + (benchyEndPos.rotationY - benchyStartPos.rotationY) * limitedScrollY;
        benchy.rotation.z = benchyStartPos.rotationZ + (benchyEndPos.rotationZ - benchyStartPos.rotationZ) * limitedScrollY;
    }
    if (arm) {
        arm.position.y = armStartPos.y + scrollY * 10;
    }
    if (extruder) {
        extruder.position.y = armStartPos.y +0.35 + scrollY * 10;
        // extruder.position.x = Math.max(-1.5, armStartPos.x + 8 - scrollY * 10.0);
        extruder.position.x = Math.max(-1.5, armStartPos.x -8 + scrollY * 8.0);
    }
}

function animate() {
    // Animate the moving lines for background effect
    lines.forEach((line, index) => {
        line.rotation.x += 0.0001 * (index + 1);  // Rotate lines at different speeds for variation
        line.rotation.y += 0.0001 * (index + 1);
    });

    renderer.render(scene, camera);
    requestAnimationFrame(animate);
}

window.addEventListener('load', init);
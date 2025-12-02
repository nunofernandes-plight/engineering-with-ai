//Prerequisites:

//npx create-react-app frontend

//cd frontend

//npm install @kitware/vtk.js

import React, { useRef, useEffect } from 'react';
import '@kitware/vtk.js/Rendering/Profiles/Geometry'; // Required for vtk.js to work
import vtkFullScreenRenderWindow from '@kitware/vtk.js/Rendering/Misc/FullScreenRenderWindow';
import vtkActor from '@kitware/vtk.js/Rendering/Core/Actor';
import vtkMapper from '@kitware/vtk.js/Rendering/Core/Mapper';
import vtkCubeSource from '@kitware/vtk.js/Filters/Sources/CubeSource';

function GeometryViewer() {
  const vtkContainerRef = useRef(null);
  const context = useRef(null);

  useEffect(() => {
    if (!context.current) {
      // 1. Setup the Render Window (The Canvas)
      const fullScreenRenderer = vtkFullScreenRenderWindow.newInstance({
        rootContainer: vtkContainerRef.current,
        containerStyle: { height: '100%', width: '100%' } // Full screen
      });
      
      const renderer = fullScreenRenderer.getRenderer();
      const renderWindow = fullScreenRenderer.getRenderWindow();

      // 2. Create a Source (The Geometry) - A Simple Cube for Week 1
      const cubeSource = vtkCubeSource.newInstance();
      
      // 3. Create Mapper (Data -> Graphics)
      const mapper = vtkMapper.newInstance();
      mapper.setInputConnection(cubeSource.getOutputPort());

      // 4. Create Actor (The Object in the Scene)
      const actor = vtkActor.newInstance();
      actor.setMapper(mapper);
      
      // 5. Add to Scene
      renderer.addActor(actor);
      renderer.resetCamera();
      renderWindow.render();

      // Store context to prevent re-initialization
      context.current = { fullScreenRenderer, renderWindow, renderer, cubeSource };
    }

    // Cleanup on unmount
    return () => {
      if (context.current) {
        context.current.fullScreenRenderer.delete();
        context.current = null;
      }
    };
  }, []);

  return (
    <div 
      ref={vtkContainerRef} 
      style={{ width: '100vw', height: '100vh', position: 'absolute', top: 0, left: 0 }} 
    />
  );
}

export default GeometryViewer;

'use client'
import React from 'react'
import DeckGL from '@deck.gl/react'
import { Map } from 'react-map-gl/maplibre'
import { GeoJsonLayer, IconLayer } from '@deck.gl/layers'
import 'maplibre-gl/dist/maplibre-gl.css'
import * as cz from '@/assets/cz.json'
import IconClusterLayer from '@/layers/icon-cluster-layer'

const INITIAL_VIEW_STATE = {
 longitude: 15.3366,
 latitude: 49.7333,
 zoom: 7,
}

export default function MapView() {
 const [mapStyle, setMapStyle] = React.useState(
  'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
 )
 const [geojson, setGeojson] = React.useState(cz)
 const [layers, setLayers] = React.useState<any[]>([])

 React.useEffect(() => {
  const loadData = async () => {
   // Assuming you have a function to fetch JSON data
   const coordinateData = await fetch(`${process.env.NEXT_PUBLIC_API}/map/`, {
    method: 'GET',
    headers: {
     'Access-Control-Allow-Origin': '*',
    },
   })
   console.log(coordinateData)

   if (!coordinateData) {
    return
   }
   updateLayers(await coordinateData.json())
  }

  loadData()
 }, [])
 const updateLayers = (coordinateData: any) => {
  setLayers([
   new GeoJsonLayer({
    id: 'CR-map-overlay',
    data: geojson,
    opacity: 0.05,
    stroked: false,
    filled: true,
    wireframe: true,
    getLineColor: [255, 255, 255],
    getFillColor: [200, 200, 200],
    pickable: true,
   }),
   new IconClusterLayer({
    id: 'icon-cluster',
    sizeScale: 40,
    data: coordinateData,
    pickable: true,
    getPosition: (d) => d.coordinates,
    iconAtlas: '/location-icon-atlas.png',
    iconMapping: '/location-icon-mapping.json',
   }),
  ])
 }

 React.useEffect(() => {
  const currentTheme = localStorage.getItem('theme')
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (currentTheme === 'dark' || (!currentTheme && prefersDarkMode)) {
   setMapStyle('https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json')
  } else {
   setMapStyle('https://basemaps.cartocdn.com/gl/positron-gl-style/style.json')
  }
 }, [])

 if (!geojson) {
  return <div>Loading...</div>
 }

 return (
  <main className="w-screen h-[95vh] mt-10">
   <DeckGL initialViewState={INITIAL_VIEW_STATE} controller={true} layers={layers}>
    <Map reuseMaps mapStyle={mapStyle} />
   </DeckGL>
  </main>
 )
}

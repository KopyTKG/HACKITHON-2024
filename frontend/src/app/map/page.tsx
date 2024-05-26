'use client'
import React from 'react'
import DeckGL from '@deck.gl/react'
import { Map } from 'react-map-gl/maplibre'
import Link from 'next/link'
import { GeoJsonLayer } from '@deck.gl/layers'
import type { IconLayerProps } from '@deck.gl/layers'
import type { PickingInfo, MapViewState } from '@deck.gl/core'
import 'maplibre-gl/dist/maplibre-gl.css'
import IconClusterLayer, { IconClusterLayerPickingInfo } from '@/layers/icon-cluster-layer'

const INITIAL_VIEW_STATE: MapViewState = {
 longitude: 15.3366,
 latitude: 49.7333,
 zoom: 7,
}

type Deska = {
 coordinates: [longitude: number, latitude: number]
 name: string
 url: string
}

function renderTooltip(info: IconClusterLayerPickingInfo<Deska>) {
 const { object, objects, x, y } = info

 if (objects) {
  return (
   <div className="mt-12 max-h-[95vh] overflow-y-scroll">
    {objects.map(({ name, url }) => {
     return (
      <div key={name} className="max-w-[10rem] h-20 bg-stone-300 text-black">
       <h5 className="text-md">{name}</h5>
       <Link href={url} target="_blank" rel="noreferrer" className="text-sm">
        Link
       </Link>
      </div>
     )
    })}
   </div>
  )
 }

 if (!object) {
  return null
 }

 return (
  'cluster' in object &&
  object.cluster && (
   <div className="tooltip" style={{ left: x, top: y }}>
    {object.point_count} records
   </div>
  )
 )
}

export default function MapView() {
 const [mapStyle, setMapStyle] = React.useState(
  'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
 )
 const [data, setData] = React.useState<Deska[]>([])
 const [layers, setLayers] = React.useState<any[]>([])
 const [hoverInfo, setHoverInfo] = React.useState<IconClusterLayerPickingInfo<Deska> | null>(null)

 const layerProps: IconLayerProps<Deska> = {
  id: 'icon',
  data,
  pickable: true,
  getPosition: (d) => d.coordinates,
  iconAtlas: '/location-icon-atlas.png',
  iconMapping: '/location-icon-mapping.json',
 }

 const hideTooltip = React.useCallback(() => {
  setHoverInfo(null)
 }, [])

 const expandTooltip = React.useCallback((info: PickingInfo) => {
  if (info.picked) {
   setHoverInfo(info)
  } else {
   setHoverInfo(null)
  }
 }, [])
 if (hoverInfo === null || !hoverInfo.objects) {
  layerProps.onHover = setHoverInfo
 }

 const updateLayers = (coordinateData: any) => {
  setLayers([
   new GeoJsonLayer({
    id: 'CR-map-overlay',
    data: '/cz.json',
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
   const tmp = await coordinateData.json()
   setData(tmp)
   updateLayers(tmp)
  }

  loadData()
 }, [updateLayers])

 React.useEffect(() => {
  const currentTheme = localStorage.getItem('theme')
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (currentTheme === 'dark' || (!currentTheme && prefersDarkMode)) {
   setMapStyle('https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json')
  } else {
   setMapStyle('https://basemaps.cartocdn.com/gl/positron-gl-style/style.json')
  }
 }, [])

 return (
  <main className="w-screen h-[95vh] mt-10">
   <DeckGL
    initialViewState={INITIAL_VIEW_STATE}
    controller={true}
    layers={layers}
    onViewStateChange={hideTooltip}
    onClick={expandTooltip}>
    <Map reuseMaps mapStyle={mapStyle} />
    {hoverInfo && renderTooltip(hoverInfo)}
   </DeckGL>
  </main>
 )
}

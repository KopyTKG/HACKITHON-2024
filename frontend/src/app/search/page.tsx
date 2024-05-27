'use client'
import React from 'react'
import Dokument, { DokumentType } from '@/components/dokument'

export default function Search() {
 const [search, setSearch] = React.useState('')
 const [dokumenty, setDokumenty] = React.useState(Array<DokumentType>)

 React.useEffect(() => {
  const searchParams = new URLSearchParams(window.location.search)
  const tmp = searchParams.get('s')
  if (tmp) setSearch(tmp)
  else setSearch('')

  async function fetchData() {
   const data = await fetch(`${process.env.NEXT_PUBLIC_API}/search`, {
    method: 'POST',
    headers: {
     'Content-Type': 'application/json',
     'Access-Control-Allow-Origin': '*',
    },
    body: JSON.stringify({ filter: tmp }),
   })

   if (data) setDokumenty(await data.json())
  }
  fetchData()
 }, [setDokumenty, setSearch])

 return (
  <main className="mt-10 py-5 px-2 max-w-6xl mx-auto flex flex-col min-h-[95vh] items-center gap-4">
   <h2 className="text-3xl font-bold text-center mb-4">
    <span className="text-stone-300 text-2xl">Vyhledáno:</span> {search}
   </h2>
   <div className="w-full h-[1px] bg-stone-400 dark:bg-stone-600" />
   <div className="w-full grid grid-cols-1 lg:grid-cols-2 gap-2">
    {dokumenty
     ? dokumenty.map((dokument: DokumentType, i: number) => (
        <Dokument
         key={i}
         nazev={dokument.nazev}
         datum={dokument.datum}
         doc_id={dokument.doc_id}
         url={dokument.url}
        />
       ))
     : Array.from({ length: 10 }).map((_, i) => (
        <div key={i} className="w-full h-20 bg-stone-300 dark:bg-stone-700" />
       ))}
   </div>
  </main>
 )
}

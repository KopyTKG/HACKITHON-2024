'use client'
import React from 'react'
import { useSearchParams } from 'next/navigation'
import Dokument from '@/components/dokument'

const mockUpAPI = (search: string) => {
 console.log('Searching for:', search)
 return new Promise((resolve) => {
  setTimeout(() => {
   resolve(
    Array.from({ length: 10 }).map((_, i) => ({
     nazev: `Název dokumentu ${i}`,
     datum: new Date(),
     doc_id: `${i}`,
    })),
   )
  }, 5000)
 })
}

export default function Search() {
 const [search, setSearch] = React.useState('')
 const [dokumenty, setDokumenty] = React.useState([])

 const searchParams = useSearchParams()

 React.useEffect(() => {
  const tmp = searchParams.get('s')
  if (tmp) setSearch(tmp)
  else setSearch('')

  async function fetchData() {
   const data = await mockUpAPI(tmp)
   if (data) setDokumenty(data)
  }
  fetchData()
 }, [searchParams, setDokumenty, setSearch])

 return (
  <main className="mt-10 py-5 px-2 max-w-6xl mx-auto flex flex-col min-h-[95vh] items-center gap-4">
   <h2 className="text-3xl font-bold text-center mb-4">
    <span className="text-stone-300 text-2xl">Vyhledáno:</span> {search}
   </h2>
   <div className="w-full h-[1px] bg-stone-400 dark:bg-stone-600" />
   <div className="w-full grid grid-cols-1 lg:grid-cols-2 gap-2">
    {dokumenty
     ? dokumenty.map((dokument, i) => <Dokument key={i} {...dokument} />)
     : Array.from({ length: 10 }).map((_, i) => (
        <div key={i} className="w-full h-20 bg-stone-300 dark:bg-stone-700" />
       ))}
   </div>
  </main>
 )
}

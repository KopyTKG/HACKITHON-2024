'use client'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import Icon from '@/components/icon'

export default function Home() {
 const categories = [
  'oznámení',
  'rozhodnutí',
  'stanovení',
  'vyhláška',
  'dražba',
  'rozpočet',
  'prodej',
  'nálezy',
  'stavební nálezy',
  'přerušení dodávek',
 ]
 const randomCategory = () => {
  const path = categories[Math.floor(Math.random() * categories.length)]
  window.location.href = `/search?s=${path}`
 }

 const search = () => {
  const search = document.querySelector('input[name="search"]') as HTMLInputElement
  if (!search.value) {
   search.classList.add('outline')
   search.classList.add('outline-2')
   search.classList.add('outline-red-500')
   setTimeout(() => {
    search.classList.remove('outline')
    search.classList.remove('outline-2')
    search.classList.remove('outline-red-500')
   }, 2000)
   return
  }
  window.location.href = `/search?s=${search.value}`
 }

 return (
  <main className="mt-10 max-w-6xl mx-auto flex flex-col min-h-[95vh] items-center justify-center gap-4">
   <h1 className="text-4xl font-bold text-center mb-4">Deska search engine</h1>
   <Input
    name="search"
    type="text"
    placeholder="Praha, Finance ..."
    className="max-w-2xl"
    required
   />
   <div className="inline-flex gap-4">
    <Button variant="neutral" onClick={() => search()}>
     Vyhledat <Icon name="search" className="w-4 ml-2" />
    </Button>
    <Button variant="neutral" onClick={() => randomCategory()}>
     Náhodný výběr <Icon name="dices" className="w-4 ml-2" />
    </Button>
   </div>
   <div className="w-full h-[1px] bg-stone-400 dark:bg-stone-600" />
   <div className="grid grid-cols-2 gap-4">
    <Button className="w-32">Oznámení</Button>
    <Button className="w-32">Rozhodnuti</Button>
    <Button className="w-32">Nálezy</Button>
    <Button className="w-32">Rozpočet</Button>
   </div>
  </main>
 )
}

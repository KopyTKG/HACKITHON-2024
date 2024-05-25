'use client'
import Icon from '@/components/icon'

export default function Dokument({
 nazev,
 datum,
 doc_id,
}: {
 nazev: string
 datum: Date
 doc_id: string
}) {
 return (
  <div className="w-full rounded-xl dark:bg-stone-700 dark:hover:bg-stone-600 bg-stone-300 hover:bg-stone-400 h-20 hover:scale-101 ease-in-out duration-100 hover:drop-shadow-xl">
   <div className="w-full inline-flex items-center gap-5 px-2">
    <Icon name="file-down" className="h-10" />
    <span className="dark:text-stone-100 text-stone-900 underline underline-offset-2 font-semibold">
     {nazev}
    </span>
   </div>
   <div className="w-full inline-flex items-center justify-between px-2">
    <span className="dark:text-stone-200 text-stone-700 inline-flex gap-[0.4rem] items-center">
     <Icon name="calendar-days" className="h-5" /> {datum.toLocaleDateString()}
    </span>
    <span className="dark:text-stone-200 text-stone-700">{doc_id}</span>
   </div>
  </div>
 )
}

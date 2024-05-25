import Link from 'next/link'
import { Button } from '@/components/ui/button'
import Icon from '@/components/icon'

export default function Navbar() {
 return (
  <nav className="w-full px-2 fixed flex top-0 bg-black/30 dark:bg-stone-500/20 backdrop-blur-xl h-10 items-center justify-end gap-2 z-[10000]">
   <Link href="/">
    <Button>
     <Icon name="home" className="w-4 mr-1" /> Domů
    </Button>
   </Link>
   <Link href="/map">
    <Button>
     <Icon name="map" className="w-4 mr-1" /> Mapa
    </Button>
   </Link>
  </nav>
 )
}

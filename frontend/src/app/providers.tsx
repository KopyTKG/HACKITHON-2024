'use client'
import react from 'react'

export default function providers({ children }: { children: react.reactnode }) {
 react.useEffect(() => {
  const currentTheme = localStorage.getItem('theme')
  const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches

  if (currentTheme === 'dark' || (!currentTheme && prefersDarkMode)) {
   document.documentElement.classList.add('dark')
   localStorage.setItem('theme', 'dark')
  } else {
   document.documentElement.classList.remove('dark')
   localStorage.setItem('theme', 'light')
  }
 }, [])

 return <>{children}</>
}

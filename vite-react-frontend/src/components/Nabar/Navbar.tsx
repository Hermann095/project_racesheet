import React from 'react'
import TopMenubar from '../TopMenubar/TopMenubar'
import TopNavigationMenu from '../TopNavigationMenu/TopNavigationMenu'

export default function Navbar() {
  return (
    <>
      <div className="fixed w-full border-b-2 border-muted bg-background">
        <div className="flex justify-between">
          <div>
            <TopMenubar />
          </div>
          <div className="flex justify-center">
            <TopNavigationMenu />
          </div>
          <div></div>
        </div>
      </div>
    </>
  )
}

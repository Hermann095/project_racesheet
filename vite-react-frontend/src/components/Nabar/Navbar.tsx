import React from 'react'
import TopMenubar from '../TopMenubar/TopMenubar'
import TopNavigationMenu from '../TopNavigationMenu/TopNavigationMenu'

export default function Navbar() {
  return (
    <>
      <div className="border-muted bg-background sticky w-full border-b-2">
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

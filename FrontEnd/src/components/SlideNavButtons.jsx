import React from 'react'
import { useSwiper } from 'swiper/react'

export default function SlideNavButtons() {
  const swiper = useSwiper()

  return (
    <div>
      <button
        onClick={() => swiper.slidePrev()}
      >
        Prev
      </button>
      <button
        onClick={() => swiper.slideNext()}
      >
        Next
      </button>
    </div>
  )
}


document.addEventListener('DOMContentLoaded', function () {
  var elems = document.querySelectorAll('.parallax');
  var paralaxPage = M.Parallax.init(elems);

  var elems = document.querySelectorAll('.pushpin');
  var pinnedNav = M.Pushpin.init(elems);

  d3.select('#refresh-data').on('click', () => {
    console.log('download data button clicked')
    d3.select('.refresh-icon').classed('hidden', true)
    d3.select('#preloader-btn').classed('hidden', false)


    d3.event.preventDefault();
    d3.json('/scrape').then((data) => {
      console.log('d3 json : ', data)
      d3.select('.refresh-icon').classed('hidden', false)
      d3.select('#preloader-btn').classed('hidden', true)
      updatePage(data)
    })
  })
});

function updatePage(data) {
  /*'news': {
  'title': latest_news_title,
    'caption': latest_news_caption
  },
  'featured_image_url': featured_image_url,
  'weather': mars_weather,
    'facts': mars_facts_table,
      'hemispheres': hemisphere_image_urls
  */
  d3.select('.news-title').text(data.news.title)
  d3.select('.news-caption').text(data.news.caption)
  d3.select('.featured_image_url').attr('src', data.featured_image_url)
  d3.select('.weather').text(data.weather)
  d3.select('.facts').html(data.facts)
  Object.values(data.hemispheres).forEach((hemi, idx) => {
    counter = idx + 1
    d3.select('.hemi-' + counter).select('img').attr('src', hemi.img_url)
    d3.select('.hemi-' + counter).select('.card-title').text(hemi.title)
  })
}

document.addEventListener('DOMContentLoaded', function () {

  // enable parallax effect
  var elems = document.querySelectorAll('.parallax');
  var parallaxPage = M.Parallax.init(elems);

  // scrape new data on button click
  d3.select('#refresh-data').on('click', () => {
    d3.event.preventDefault();
    getData();
  });

});

// retrieve data from the web
function getData() {
  let isLoading = true;
  updateLoader(isLoading)

  d3.json('/scrape').then(data => {
    isLoading = false;
    updateLoader(isLoading);
    updatePage(data);
  });

}

function updateLoader(isLoading) {
  d3.select('.refresh-icon').classed('hidden', isLoading);
  d3.select('#preloader-btn').classed('hidden', !isLoading);
}

function updatePage(data) {

  d3.select('.news-title').text(data.news_title)
  d3.select('.news-caption').text(data.news_caption)

  d3.select('.featured_image_url').attr('src', data.featured_image_url)

  d3.select('.weather').text(data.weather)

  d3.select('.facts').html(data.facts)

  d3.select('#results')
    .selectAll('.col,.s12,.m6')
    .data(data.hemispheres)
    .enter()
    .append('div')
    .attr('class', 'col s12 m6')
    .each(function (item) {
      d3.select(this).html(
        `<div class="card hoverable">
        <div class="card-image">
          <img src="${item.img_url}">
        </div>
        <div class="card-content">
          <span class="card-title grey-text text-darken-4">${item.title}</span>
        </div></div>`)
    })
}

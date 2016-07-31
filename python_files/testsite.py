from xml.dom import minidom
html_file = """
 
<div class="container-fluid" id="first-quotes">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>100</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/j/johnkeats386110.html">
I love you the more in that I believe you had liked me for my own sake and for nothing else.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/j/john_keats.html">
John Keats
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>99</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/e/ernesthemi152926.html">
But man is not made for defeat. A man can be destroyed but not defeated.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/e/ernest_hemingway.html">
Ernest Hemingway
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>98</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/f/franklind101840.html">
When you reach the end of your rope, tie a knot in it and hang on.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/f/franklin_d_roosevelt.html">
Franklin D. Roosevelt
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>97</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/h/heraclitus165537.html">
There is nothing permanent except change.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/h/heraclitus.html">
Heraclitus
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>96</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/e/elizabethb163270.html">
My sun sets to rise again.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/e/elizabeth_barrett_brownin.html">
Elizabeth Barrett Browning
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>95</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/apjabdu178504.html">
Let us sacrifice our today so that our children can have a better tomorrow.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/a_p_j_abdul_kalam.html">
A. P. J. Abdul Kalam
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-1.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>94</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/n/niccolomac103757.html">
It is better to be feared than loved, if you cannot be both.
</a>
<cite>
<a href="/quotes/authors/n/niccolo_machiavelli.html">
Niccolo Machiavelli
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-8 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>93</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/ameliaearh120929.html">
The most difficult thing is the decision to act, the rest is merely tenacity. The fears are paper tigers. You can do anything you decide to do. You can act to change and control your life; and the procedure, the process is its own reward.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/amelia_earhart.html">
Amelia Earhart
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>92</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/h/henryjames157154.html">
Do not mind anything that anyone tells you about anyone else. Judge everyone and everything for yourself.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/h/henry_james.html">
Henry James
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>90</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/j/janeausten395520.html">
There is no charm equal to tenderness of heart.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/j/jane_austen.html">
Jane Austen
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>89</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/e/edgarallan109738.html">
All that we see or seem is but a dream within a dream.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/e/edgar_allan_poe.html">
Edgar Allan Poe
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>88</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/f/francisofa389169.html">
Lord, make me an instrument of thy peace. Where there is hatred, let me sow love.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/f/francis_of_assisi.html">
Francis of Assisi
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="isotope-grid style-masonry" data-heightratio="0.9">
<div class="isotope-item wide">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-1.jpg" alt="Picture Quote - The only journey is the one within. Rainer Maria Rilke">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>87</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/r/rainermari147758.html">
The only journey is the one within.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/r/rainer_maria_rilke.html">
Rainer Maria Rilke
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-1.jpg" alt="Picture Quote - Good judgment comes from experience, and a lot of that comes from bad judgment. Will Rogers">
<div class="overlay-caption caption-top text-light">
<div class="listPositionNumLight">
<span>86</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/w/willrogers411692.html">
Good judgment comes from experience, and a lot of that comes from bad judgment.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/w/will_rogers.html">
Will Rogers
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-tall-1.jpg" alt="Picture Quote - Think in the morning. Act in the noon. Eat in the evening. Sleep in the night. William Blake">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>85</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/w/williambla150142.html">
Think in the morning. Act in the noon. Eat in the evening. Sleep in the night.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/w/william_blake.html">
William Blake
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-square-1.jpg" alt="Picture Quote - Life without love is like a tree without blossoms or fruit. Khalil Gibran">
<div class="overlay-caption caption-bottom">
<div class="listPositionNumLight">
<span>84</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/k/khalilgibr100719.html">
Life without love is like a tree without blossoms or fruit.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/k/khalil_gibran.html">
Khalil Gibran
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-2.jpg" alt="Picture Quote - No act of kindness, no matter how small, is ever wasted. Aesop">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>83</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/a/aesop109734.html">
No act of kindness, no matter how small, is ever wasted.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/a/aesop.html">
Aesop
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-2.jpg" alt="Picture Quote - Love cures people - both the ones who give it and the ones who receive it. Karl A. Menninger">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>82</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/k/karlamenn161526.html">
Love cures people - both the ones who give it and the ones who receive it.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/k/karl_a_menninger.html">
Karl A. Menninger
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-3.jpg" alt="Picture Quote - Work like you don't need the money. Love like you've never been hurt. Dance like nobody's watching. Satchel Paige">
<div class="overlay-caption caption-bottom">
<div class="listPositionNumLight">
<span>81</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/s/satchelpai390217.html">
Work like you don't need the money. Love like you've never been hurt. Dance like nobody's watching.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/s/satchel_paige.html">
Satchel Paige
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-4.jpg" alt="Picture Quote - It is far better to be alone, than to be in bad company. George Washington">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>80</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/g/georgewash109673.html">
It is far better to be alone, than to be in bad company.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/g/george_washington.html">
George Washington
</a>
</span>
</div>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>79</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/n/napoleonhi152848.html">
If you cannot do great things, do small things in a great way.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/n/napoleon_hill.html">
Napoleon Hill
</a>
</div>
</div>
</div>
<div class="col-md-8 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>78</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/t/thomascarl156180.html">
Permanence, perseverance and persistence in spite of all obstacles, discouragements, and impossibilities: It is this, that in all things distinguishes the strong soul from the weak.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/t/thomas_carlyle.html">
Thomas Carlyle
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>77</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/s/susanbant380664.html">
Independence is happiness.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/s/susan_b_anthony.html">
Susan B. Anthony
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>76</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/s/suntzu383158.html">
The supreme art of war is to subdue the enemy without fighting.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/s/sun_tzu.html">
Sun Tzu
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>75</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/w/waltwhitma384665.html">
Keep your face always toward the sunshine - and shadows will fall behind you.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/w/walt_whitman.html">
Walt Whitman
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-3.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>74</span>
</div>
<div>
<blockquote> <a href="/quotes/quotes/s/sigmundfre151780.html">
Being entirely honest with oneself is a good exercise.
</a>
<cite>
<a href="/quotes/authors/s/sigmund_freud.html">
Sigmund Freud
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>73</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/g/georgeorwe119587.html">
Happiness can exist only in acceptance.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/g/george_orwell.html">
George Orwell
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>72</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/j/johngalswo380209.html">
Love has no age, no limit; and no death.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/j/john_galsworthy.html">
John Galsworthy
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>71</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/alberteins417379.html">
You can't blame gravity for falling in love.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/albert_einstein.html">
Albert Einstein
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>70</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/aldoushuxl386738.html">
There is only one corner of the universe you can be certain of improving, and that's your own self.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/aldous_huxley.html">
Aldous Huxley
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>69</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/t/thomasjeff101007.html">
Honesty is the first chapter in the book of wisdom.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/t/thomas_jefferson.html">
Thomas Jefferson
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>68</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/l/laotzu137141.html">
The journey of a thousand miles begins with one step.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/l/lao_tzu.html">
Lao Tzu
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="isotope-grid style-masonry" data-heightratio="0.9">
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-3.jpg" alt="Picture Quote - The best preparation for tomorrow is doing your best today. H. Jackson Brown, Jr.">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>67</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/h/hjacksonb382774.html">
<a href="/quotes/quotes/h/hjacksonb382774.html">
The best preparation for tomorrow is doing your best today.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/h/h_jackson_brown_jr.html">
H. Jackson Brown, Jr.
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-2.jpg" alt="Picture Quote - A new command I give you: Love one another. As I have loved you, so you must love one another. Jesus Christ">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>66</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/j/jesuschris414650.html">
<a href="/quotes/quotes/j/jesuschris414650.html">
A new command I give you: Love one another. As I have loved you, so you must love one another.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/j/jesus_christ.html">
Jesus Christ
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-square-5.jpg" alt="Picture Quote - There are two ways of spreading light: to be the candle or the mirror that reflects it. Edith Wharton">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>65</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/e/edithwhart100511.html">
<a href="/quotes/quotes/e/edithwhart100511.html">
There are two ways of spreading light: to be the candle or the mirror that reflects it.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/e/edith_wharton.html">
Edith Wharton
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-tall-2.jpg" alt="Picture Quote - Ever tried. Ever failed. No matter. Try Again. Fail again. Fail better. Samuel Beckett">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>64</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/s/samuelbeck121335.html">
<a href="/quotes/quotes/s/samuelbeck121335.html">
Ever tried. Ever failed. No matter. Try Again. Fail again. Fail better.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/s/samuel_beckett.html">
Samuel Beckett
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-tall-3.jpg" alt="Picture Quote - God gave us the gift of life; it is up to us to give ourselves the gift of living well. Voltaire">
<div class="overlay-caption caption-bottom">
<div class="listPositionNumLight">
<span>63</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/v/voltaire134077.html">
<a href="/quotes/quotes/v/voltaire134077.html">
God gave us the gift of life; it is up to us to give ourselves the gift of living well.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/v/voltaire.html">
Voltaire
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-3.jpg" alt="Picture Quote - Do all things with love. Og Mandino">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>62</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/o/ogmandino100726.html">
<a href="/quotes/quotes/o/ogmandino100726.html">
Do all things with love.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/o/og_mandino.html">
Og Mandino
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-square-6.jpg" alt="Picture Quote - Change your life today. Don't gamble on the future, act now, without delay. Simone de Beauvoir">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>61</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/s/simonedebe149611.html">
<a href="/quotes/quotes/s/simonedebe149611.html">
Change your life today. Don't gamble on the future, act now, without delay.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/s/simone_de_beauvoir.html">
Simone de Beauvoir
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-4.jpg" alt="Picture Quote - Not all those who wander are lost. J. R. R. Tolkien">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>60</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/j/jrrtolk101490.html">
<a href="/quotes/quotes/j/jrrtolk101490.html">
Not all those who wander are lost.
</a>
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/j/j_r_r_tolkien.html">
J. R. R. Tolkien
</a>
</span>
</div>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>59</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/annefrank145726.html">
Whoever is happy will make others happy too.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/anne_frank.html">
Anne Frank
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>58</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/t/thomasaed132683.html">
I have not failed. I've just found 10,000 ways that won't work.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/t/thomas_a_edison.html">
Thomas A. Edison
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>57</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/b/benjaminfr383997.html">
Tell me and I forget. Teach me and I remember. Involve me and I learn.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/b/benjamin_franklin.html">
Benjamin Franklin
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>56</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/t/thomasaqui163328.html">
There is nothing on this earth more to be prized than true friendship.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/t/thomas_aquinas.html">
Thomas Aquinas
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>55</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/j/johncmaxw383606.html">
A leader is one who knows the way, goes the way, and shows the way.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/j/john_c_maxwell.html">
John C. Maxwell
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>54</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/marcusaure386395.html">
Very little is needed to make a happy life; it is all within yourself, in your way of thinking.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/marcus_aurelius.html">
Marcus Aurelius
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-3.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>53</span>
</div>
<div>
<blockquote> <a href="/quotes/quotes/g/georgesand383232.html">
There is only one happiness in this life, to love and be loved.
</a>
<cite>
<a href="/quotes/authors/g/george_sand.html">
George Sand
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>52</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/miltonberl105306.html">
If opportunity doesn't knock, build a door.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/milton_berle.html">
Milton Berle
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>51</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/marktwain118964.html">
The secret of getting ahead is getting started.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/mark_twain.html">
Mark Twain
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>50</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/marcelprou105251.html">
Let us be grateful to people who make us happy, they are the charming gardeners who make our souls blossom.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/marcel_proust.html">
Marcel Proust
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>49</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/margaretme141040.html">
Always remember that you are absolutely unique. Just like everyone else.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/margaret_mead.html">
Margaret Mead
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>48</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/p/plato109439.html">
Wise men speak because they have something to say; Fools because they have to say something.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/p/plato.html">
Plato
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>47</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/j/johnquincy386752.html">
If your actions inspire others to dream more, learn more, do more and become more, you are a leader.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/j/john_quincy_adams.html">
John Quincy Adams
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="isotope-grid style-masonry" data-heightratio="0.9">
<div class="isotope-item wide">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-2.jpg" alt="Picture Quote - When we are no longer able to change a situation - we are challenged to change ourselves. Viktor E. Frankl">
<div class="overlay-caption caption-bottom">
<div class="listPositionNumLight">
<span>46</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/v/viktorefr121087.html">
When we are no longer able to change a situation - we are challenged to change ourselves.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/v/viktor_e_frankl.html">
Viktor E. Frankl
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-3.jpg" alt="Picture Quote - Problems are not stop signs, they are guidelines. Robert H. Schuller">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>45</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/r/roberthsc107067.html">
Problems are not stop signs, they are guidelines.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/r/robert_h_schuller.html">
Robert H. Schuller
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-tall-2.jpg" alt="Picture Quote - What we achieve inwardly will change outer reality. Plutarch">
<div class="overlay-caption caption-top text-light">
<div class="listPositionNumLight">
<span>44</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/p/plutarch120365.html">
What we achieve inwardly will change outer reality.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/p/plutarch.html">
Plutarch
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-4.jpg" alt="Picture Quote - Spread love everywhere you go. Let no one ever come to you without leaving happier. Mother Teresa">
<div class="overlay-caption caption-top">
<div class="listPositionNumLight">
<span>43</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/m/mothertere133195.html">
Spread love everywhere you go. Let no one ever come to you without leaving happier.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/m/mother_teresa.html">
Mother Teresa
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-1.jpg" alt="Picture Quote - We love life, not because we are used to living but because we are used to loving. Friedrich Nietzsche">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>42</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/f/friedrichn103522.html">
We love life, not because we are used to living but because we are used to loving.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/f/friedrich_nietzsche.html">
Friedrich Nietzsche
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-1.jpg" alt="Picture Quote - All our dreams can come true, if we have the courage to pursue them. Walt Disney">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>41</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/w/waltdisney163027.html">
All our dreams can come true, if we have the courage to pursue them.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/w/walt_disney.html">
Walt Disney
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-3.jpg" alt="Picture Quote - We know what we are, but know not what we may be. William Shakespeare">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>40</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/w/williamsha164317.html">
We know what we are, but know not what we may be.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/w/william_shakespeare.html">
William Shakespeare
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-5.jpg" alt="Picture Quote - It's not what you look at that matters, it's what you see. Henry David Thoreau">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>39</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/h/henrydavid106041.html">
It's not what you look at that matters, it's what you see.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/h/henry_david_thoreau.html">
Henry David Thoreau
</a>
</span>
</div>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>38</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/l/leobuscagl163836.html">
A single rose can be my garden... a single friend, my world.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/l/leo_buscaglia.html">
Leo Buscaglia
</a>
</div>
</div>
</div>
<div class="col-md-8 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>37</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/s/swamivivek213397.html">
Take up one idea. Make that one idea your life - think of it, dream of it, live on that idea. Let the brain, muscles, nerves, every part of your body, be full of that idea, and just leave every other idea alone. This is the way to success.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/s/swami_vivekananda.html">
Swami Vivekananda
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>36</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/e/euripides149013.html">
Friends show their love in times of trouble, not in happiness.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/e/euripides.html">
Euripides
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>35</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/d/desmondtut112366.html">
You don't choose your family. They are God's gift to you, as you are to them.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/d/desmond_tutu.html">
Desmond Tutu
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>34</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/s/sorenkierk414008.html">
Life is not a problem to be solved, but a reality to be experienced.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/s/soren_kierkegaard.html">
Soren Kierkegaard
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-4.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>33</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/g/georgebern109542.html">
Life isn't about finding yourself. Life is about creating yourself.
</a>
<cite>
<a href="/quotes/authors/g/george_bernard_shaw.html">
George Bernard Shaw
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>32</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/s/socrates101212.html">
The only true wisdom is in knowing you know nothing.
</a>
<cite>
<a href="/quotes/authors/s/socrates.html">
Socrates
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-5.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>31</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/c/confucius104254.html">
Everything has beauty, but not everyone sees it.
</a>
<cite>
<a href="/quotes/authors/c/confucius.html">
Confucius
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>30</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/i/ingridberg103428.html">
A kiss is a lovely trick designed by nature to stop speech when words become superfluous.
</a>
<cite>
<a href="/quotes/authors/i/ingrid_bergman.html">
Ingrid Bergman
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="isotope-grid style-masonry" data-heightratio="0.9">
<div class="isotope-item wide">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-3.jpg" alt="Picture Quote - For it was not into my ear you whispered, but into my heart. It was not my lips you kissed, but my soul. Judy Garland">
<div class="overlay-caption caption-bottom">
<div class="listPositionNumLight">
<span>29</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/j/judygarlan100718.html">
For it was not into my ear you whispered, but into my heart. It was not my lips you kissed, but my soul.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/j/judy_garland.html">
Judy Garland
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-1.jpg" alt="Picture Quote - If you live to be a hundred, I want to live to be a hundred minus one day so I never have to live without you. A. A. Milne">
<div class="overlay-caption caption-top text-light">
<div class="listPositionNumLight">
<span>28</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/a/aamilne163067.html">
If you live to be a hundred, I want to live to be a hundred minus one day so I never have to live without you.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/a/a_a_milne.html">
A. A. Milne
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-tall-2.jpg" alt="Picture Quote - As we express our gratitude, we must never forget that the highest appreciation is not to utter words, but to live by them. John F. Kennedy">
<div class="overlay-caption caption-top text-light">
<div class="listPositionNumLight">
<span>27</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/j/johnfkenn105511.html">
As we express our gratitude, we must never forget that the highest appreciation is not to utter words, but to live by them.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/j/john_f_kennedy.html">
John F. Kennedy
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-4.jpg" alt="Picture Quote - Life's most persistent and urgent question is, 'What are you doing for others?' Martin Luther King, Jr.">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>26</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/m/martinluth137105.html">
Life's most persistent and urgent question is, 'What are you doing for others?'
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/m/martin_luther_king_jr.html">
Martin Luther King, Jr.
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item wide tall">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-1 text-light">
<img src="/st/img/1833865/top_100/masonry-wide-tall-3.jpg" alt="Picture Quote - Believe you can and you're halfway there. Theodore Roosevelt">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>25</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/t/theodorero380703.html">
Believe you can and you're halfway there.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/t/theodore_roosevelt.html">
Theodore Roosevelt
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-1.jpg" alt="Picture Quote - Happiness resides not in possessions, and not in gold, happiness dwells in the soul. Democritus">
<div class="overlay-caption caption-bottom text-light">
<div class="listPositionNumLight">
<span>24</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/d/democritus154879.html">
Happiness resides not in possessions, and not in gold, happiness dwells in the soul.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/d/democritus.html">
Democritus
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-5.jpg" alt="Picture Quote - The pessimist complains about the wind; the optimist expects it to change; the realist adjusts the sails. William Arthur Ward">
<div class="overlay-caption">
<div class="listPositionNumLight">
<span>23</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/w/williamart110212.html">
The pessimist complains about the wind; the optimist expects it to change; the realist adjusts the sails.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/w/william_arthur_ward.html">
William Arthur Ward
</a>
</span>
</div>
</div>
</div>
</div>
<div class="isotope-item make-small">
<div class="masonry-media">
<div class="thumb-overlay overlay-effect-3 text-light">
<img src="/st/img/1833865/top_100/masonry-square-2.jpg" alt="Picture Quote - The future belongs to those who believe in the beauty of their dreams. Eleanor Roosevelt">
<div class="overlay-caption text-light">
<div class="listPositionNumLight">
<span>22</span>
</div>
<span class="masonry-quote">
<a href="/quotes/quotes/e/eleanorroo100940.html">
The future belongs to those who believe in the beauty of their dreams.
</a>
</span>
<span class="masonry-author">
<a href="/quotes/authors/e/eleanor_roosevelt.html">
Eleanor Roosevelt
</a>
</span>
</div>
</div>
</div>
</div>
</div>
 
 
<div class="container-fluid" id="test">
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>21</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/d/drseuss414098.html">
Today you are you! That is truer than true! There is no one alive who is you-er than you!
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/d/dr_seuss.html">
Dr. Seuss
</a>
</div>
</div>
</div>
<div class="col-md-8 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>20</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/n/nelsonmand157855.html">
Education is the most powerful weapon which you can use to change the world.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/n/nelson_mandela.html">
Nelson Mandela
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>19</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/n/normanvinc130593.html">
Change your thoughts and you change your world.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/n/norman_vincent_peale.html">
Norman Vincent Peale
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>18</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/mahatmagan100717.html">
Where there is love there is life.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/mahatma_gandhi.html">
Mahatma Gandhi
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>17</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/l/lorettayou195830.html">
Love isn't something you find. Love is something that finds you.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/l/loretta_young.html">
Loretta Young
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>16</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/albertcamu100779.html">
Don't walk behind me; I may not lead. Don't walk in front of me; I may not follow. Just walk beside me and be my friend.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/albert_camus.html">
Albert Camus
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>15</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/abrahamlin137180.html">
In the end, it's not the years in your life that count. It's the life in your years.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/abraham_lincoln.html">
Abraham Lincoln
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>14</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/w/winstonchu124653.html">
Success is not final, failure is not fatal: it is the courage to continue that counts.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/w/winston_churchill.html">
Winston Churchill
</a>
</div>
</div>
</div>
</div>
 
<div class="row">
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-dark-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>13</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/r/ralphwaldo101322.html">
Do not go where the path may lead, go instead where there is no path and leave a trail.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/r/ralph_waldo_emerson.html">
Ralph Waldo Emerson
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-light-grey" style="margin-top: 0px;">
<div class="listPositionNum">
<span>12</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/a/aristotle143026.html">
Love is composed of a single soul inhabiting two bodies.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/a/aristotle.html">
Aristotle
</a>
</div>
</div>
</div>
<div class="col-md-4 no-pad">
<div class="col-content quote-text-block block-white" style="margin-top: 0px;">
<div class="listPositionNum">
<span>11</span>
</div>
<span class="block-quote">
<a href="/quotes/quotes/m/mayaangelo578763.html">
Try to be a rainbow in someone's cloud.
</a>
</span>
<div class="block-author">
<a href="/quotes/authors/m/maya_angelou.html">
Maya Angelou
</a>
</div>
</div>
</div>
</div>
 
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-6.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>10</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/l/luciusanna155059.html">
One of the most beautiful qualities of true friendship is to understand and to be understood.
</a>
<cite>
<a href="/quotes/authors/l/lucius_annaeus_seneca.html">
Lucius Annaeus Seneca
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>9</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/e/edmundburk377528.html">
The only thing necessary for the triumph of evil is for good men to do nothing.
</a>
<cite>
<a href="/quotes/authors/e/edmund_burke.html">
Edmund Burke
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-7.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>8</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/b/buddha101052.html">
Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.
</a>
<cite>
<a href="/quotes/authors/b/buddha.html">
Buddha
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>7</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/r/robertloui101230.html">
Don't judge each day by the harvest you reap but by the seeds that you plant.
</a>
<cite>
<a href="/quotes/authors/r/robert_louis_stevenson.html">
Robert Louis Stevenson
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-8.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>6</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/a/audreyhepb413479.html">
Nothing is impossible, the word itself says 'I'm possible'!
</a>
<cite>
<a href="/quotes/authors/a/audrey_hepburn.html">
Audrey Hepburn
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>5</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/j/josephcamp384345.html">
Find a place inside where there's joy, and the joy will burn out the pain.
</a>
<cite>
<a href="/quotes/authors/j/joseph_campbell.html">
Joseph Campbell
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-9.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>4</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/c/cslewis119176.html">
You are never too old to set another goal or to dream a new dream.
</a>
<cite>
<a href="/quotes/authors/c/c_s_lewis.html">
C. S. Lewis
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>3</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/a/aristotleo119068.html">
It is during our darkest moments that we must focus to see the light.
</a>
<cite>
<a href="/quotes/authors/a/aristotle_onassis.html">
Aristotle Onassis
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-light parallax-section lazy" data-original="/st/img/1833865/top_100/parallax-10.jpg">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNumLight">
<span>2</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/o/oscarwilde121811.html">
Keep love in your heart. A life without it is like a sunless garden when the flowers are dead.
</a>
<cite>
<a href="/quotes/authors/o/oscar_wilde.html">
Oscar Wilde
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
 
 
<div class="fullwidth-section text-dark">
<div class="fullwidth-content wrapper-small align-center">
<div>
<div class="listPositionNum">
<span>1</span>
</div>
<div>
<blockquote>
<a href="/quotes/quotes/h/helenkelle101301.html">
The best and most beautiful things in the world cannot be seen or even touched - they must be felt with the heart.
</a>
<cite>
<a href="/quotes/authors/h/helen_keller.html">
Helen Keller
</a>
</cite>
</blockquote>
</div>
</div>
</div>
</div>
"""

print minidom.parseString(html_file)


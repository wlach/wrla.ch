    Title: Back to WordPerfect: libwpd 0.9.0
    Date: 2010-11-17T00:00:00
    Tags: Free Software

Those who've known me for a while have probably heard about my first major open source project, [libwpd][1]. In a nutshell, it's a parser for WordPerfect documents with the primary aim of converting them into something usable by the major opensource office programs out there. It's used by [LibreOffice][2], [OpenOffice.org][3], [AbiWord][4], and [KOffice][5]. WordPerfect isn't the most popular word processor out there, but there's still quite a number of legacy documents in that format, especially in the legal community (which was almost exclusively using WordPerfect until very recently).

This project goes way back: I started work on it with Marc Maurer way back in 2002 (just after I graduated from University). I put a rather ridiculous amount of unpaid work into it for a few years. WordPerfect's streaming document format is a bit esoteric to say the least, and figuring out how to map into the document model used by more modern software was a pretty interesting problem. I still remember spending sleepless nights trying to reliably convert WordPerfect's outlining into structured lists (I mostly succeeded).

Since then, I've mostly moved on to other things, leaving the project in the capable hands of [Fridrich Strba][6], who's been steadily working on adding a number of important features to the library that massively improve import fidelity. I did have time this summer to add page numbering support (thanks to [Yam Software][7] for sponsoring that work) and move the project over to git from cvs, but for the most part it's been his show since late 2004.

Even if I'm not as actively involved as I once was, when there's major developments, I still get excited (perhaps in the way that a parent might about a child who's left the household). And yesterday brought something pretty big: [libwpd 0.9.0][8]. With this release, we finally supports graphics (thanks to the work of Fridrich and Ariya Hidayat on [libwpg][9]), notes, the page numbering that I mentioned above, and support for encrypted documents. It's a big deal. Here's some before and after screenshots:

<table>
  <tr>
    <td>
      <a href="/files/2010/11/libwpd_screenshot_graphic_0.8.png"><br /> <img src="/files/2010/11/libwpd_screenshot_graphic_0.8_thumb.png" alt="libwpd_screenshot_graphic_0.8_thumb" title="libwpd_screenshot_graphic_0.8_thumb" width="200" height="163" class="alignleft size-full wp-image-148" /></a>
    </td>
    
    <td>
      <a href="/files/2010/11/libwpd_screenshot_graphic_0.9.png"><br /> <img src="/files/2010/11/libwpd_screenshot_graphic_0.9_thumb.png" alt="libwpd_screenshot_graphic_0.9_thumb" title="libwpd_screenshot_graphic_0.9_thumb" width="200" height="152" class="alignleft size-full wp-image-151" /><br /> </a>
    </td>
  </tr>
  
  <tr>
    <td>
      <a href="/files/2010/11/libwpd_screenshot_note_0.8.png"><br /> <img src="/files/2010/11/libwpd_screenshot_note_0.8_thumb.png" alt="libwpd_screenshot_note_0.8_thumb" title="libwpd_screenshot_note_0.8_thumb" width="200" height="163" class="alignleft size-full wp-image-148" /></a>
    </td>
    
    <td>
      <a href="/files/2010/11/libwpd_screenshot_note_0.9.png"><br /> <img src="/files/2010/11/libwpd_screenshot_note_0.9_thumb.png" alt="libwpd_screenshot_note_0.9_thumb" title="libwpd_screenshot_note_0.9_thumb" width="200" height="152" class="alignleft size-full wp-image-151" /><br /> </a>
    </td>
  </tr>
  
  <tr>
    <td>
      <a href="/files/2010/11/libwpd_screenshot_page_numbering_0.8.png"><br /> <img src="/files/2010/11/libwpd_screenshot_page_numbering_0.8_thumb.png" alt="libwpd_screenshot_page_numbering_0.8_thumb" title="libwpd_screenshot_page_numbering_0.8_thumb" width="200" height="163" class="alignleft size-full wp-image-148" /></a>
    </td>
    
    <td>
      <a href="/files/2010/11/libwpd_screenshot_page_numbering_0.9.png"><br /> <img src="/files/2010/11/libwpd_screenshot_page_numbering_0.9_thumb.png" alt="libwpd_screenshot_note_0.9_thumb" title="libwpd_screenshot_page_numbering_0.9_thumb" width="200" height="152" class="alignleft size-full wp-image-151" /><br /> </a>
    </td>
  </tr>
</table>

All this goodness should be available transparently whenever you import a WordPerfect file in an upcoming release of [LibreOffice][2]. AbiWord and KOffice filters should come soon enough as well (the updates needed to support libwpd 0.9 are fairly minimal).

Integration with OpenOffice.org is another story. Without going into great amount of detail on the situation (see [this article][10] on Ars Technica for the gory details if you're really interested), it's quite unlikely that OpenOffice.org WordPerfect support will advance unless (1) someone volunteers to do it and (2) Oracle drops their copyright assignment policy. The chances of these things happening seem rather low to me. My personal recommendation would be to switch to [LibreOffice][2] as soon as the first production version is released. I expect it to rapidly overtake OpenOffice.org in functionality due to its more open participation model.

[1]: http://libwpd.sourceforge.net
[2]: http://libreoffice.org
[3]: http://openoffice.org
[4]: http://abisource.com
[5]: http://koffice.org
[6]: http://fridrich.blogspot.com
[7]: http://www.yamsoftware.com
[8]: http://libwpd.sourceforge.net/news.html
[9]: http://libwpg.sourceforge.net
[10]: http://arstechnica.com/open-source/news/2010/09/document-foundation-forks-openofficeorg-to-liberate-it-from-oracle.ars
